#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 0:27
# @Author  : Suzuran
# @FileName: rest_api.py
# @Software: PyCharm
import os
import asyncio
import base64

from .articles import get_all_articles, normalize_title
from .tags import get_all_tags
from .categories import get_all_categories
from .update import _update_article
from .create import _create_article
from .utils import DEFAULT_TIMEOUT
from .rate_limiter import RateLimiter
from .progress_manager import ProgressManager


class RestApi:
    def __init__(
        self,
        url: str,
        wp_username=None,
        wp_password=None,
        timeout=DEFAULT_TIMEOUT,
        rate_limiter=None,
        progress_manager=None,
    ):
        self.url = url if url.endswith("/") else url + "/"
        self.wp_header = {
            "Authorization": "Basic "
            + base64.b64encode(f"{wp_username}:{wp_password}".encode()).decode("utf-8")
        }
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.article_title_dict = {}
        self.categories_dict = {}
        self.tags_dict = {}
        self.rate_limiter = rate_limiter
        self.progress_manager = progress_manager

    async def upload_article(
        self,
        md_message=None,
        post_metadata=None,
        verbose=True,
        force_upload=False,
        last_update=False,
    ):
        """
        自动判断更新还是创建
        @param last_update: 是否更新文章最后更新时间
        @param verbose: 是否输出控制台信息
        @param force_upload: 是否启用强制上传
        @param post_metadata: 上传文件的元信息
        @param md_message: 需要更新的md文件路径信息
        @return:
        """

        # 输出速率限制器信息
        if self.rate_limiter and verbose:
            print(
                f"Rate limiter enabled: {self.rate_limiter.request_delay}s delay per request, "
                f"batch size {self.rate_limiter.batch_size}"
            )

        # 输出进度管理器信息
        if self.progress_manager and verbose:
            print(f"Progress manager enabled: {self.progress_manager.progress_file}")

        # 更新现有文章信息
        articles_async = asyncio.create_task(get_all_articles(self, verbose))
        tags_async = asyncio.create_task(get_all_tags(self, verbose))
        categories_async = asyncio.create_task(get_all_categories(self, verbose))

        await categories_async
        await tags_async
        await articles_async

        md_create = md_message['new']
        md_update = md_message['legacy']

        None if not verbose else print(
            "You don't want a force uploading. The existence of the post would be checked."
        ) if not force_upload else print("You want a force uploading? Great!")

        # 合并所有需要处理的文件
        all_files = []
        for f in md_create:
            all_files.append(('create', f))
        for f in md_update:
            all_files.append(('update', f))

        total_files = len(all_files)

        # 如果有进度管理器，加载断点
        start_index = 0
        if self.progress_manager:
            start_index = self.progress_manager.get_resume_index()
            if start_index > 0:
                all_files = all_files[start_index:]
                if verbose:
                    print(f"Resuming from index {start_index}, {len(all_files)} files remaining")

        # 获取批次大小
        batch_size = self.rate_limiter.batch_size if self.rate_limiter else total_files

        # 分批处理
        for batch_start in range(0, len(all_files), batch_size):
            batch_end = min(batch_start + batch_size, len(all_files))
            current_batch = all_files[batch_start:batch_end]

            if verbose and self.rate_limiter:
                batch_num = (batch_start + start_index) // batch_size + 1
                total_batches = (total_files + batch_size - 1) // batch_size
                print(
                    f"\n[Batch {batch_num}/{total_batches}] Processing files "
                    f"{batch_start + start_index + 1}-{batch_end + start_index}..."
                )

            # 处理当前批次
            for i, (operation, md_file) in enumerate(current_batch):
                global_index = batch_start + i + start_index

                # 检查是否已上传（断点续传）
                if self.progress_manager and self.progress_manager.should_skip(md_file):
                    if verbose:
                        print(f"  [{global_index + 1}/{total_files}] Skipping {md_file} (already uploaded)")
                    continue

                filename_prefix = normalize_title(os.path.splitext(os.path.basename(md_file))[0])

                # 请求前延迟
                if self.rate_limiter:
                    await self.rate_limiter.wait_before_request(i)

                # 执行上传/更新（带 429 重试）
                try:
                    await self._upload_with_retry(
                        operation=operation,
                        md_file=md_file,
                        filename_prefix=filename_prefix,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload,
                        last_update=last_update,
                    )

                    # 标记完成
                    if self.progress_manager:
                        self.progress_manager.mark_completed(md_file)

                except Exception as e:
                    # 标记失败
                    if self.progress_manager:
                        self.progress_manager.mark_failed(md_file, str(e))
                    raise

                # 保存进度
                if self.progress_manager:
                    self.progress_manager.save(
                        total=total_files,
                        completed=[],
                        failed=[],
                        current_index=global_index + 1,
                    )

            # 批次间延迟
            if self.rate_limiter and batch_end < len(all_files):
                if verbose:
                    print(
                        f"Batch completed. Pausing for {self.rate_limiter.batch_delay}s before next batch..."
                    )
                await asyncio.sleep(self.rate_limiter.batch_delay)

        # 全部完成，清空进度
        if self.progress_manager:
            self.progress_manager.clear()

    async def _upload_with_retry(
        self,
        operation: str,
        md_file: str,
        filename_prefix: str,
        post_metadata,
        verbose: bool,
        force_upload: bool,
        last_update: bool,
    ):
        """
        带 429 重试的上传逻辑

        Args:
            operation: 'create' 或 'update'
            md_file: Markdown 文件路径
            filename_prefix: 标准化后的文件名（不含扩展名）
            post_metadata: 文章元数据
            verbose: 是否输出详细日志
            force_upload: 是否强制上传
            last_update: 是否更新最后修改时间
        """
        retry_count = 0
        max_retries = self.rate_limiter.max_429_retries if self.rate_limiter else 0

        while True:
            try:
                if operation == 'create':
                    if not force_upload:
                        if filename_prefix in self.article_title_dict:
                            if verbose:
                                print(
                                    f'Warning: The post {md_file} is existed in your WordPress site. Ignore uploading!'
                                )
                            return
                        else:
                            if verbose:
                                print(
                                    f'The post {md_file} is exactly a new one in your WordPress site! Try uploading...'
                                )
                            _create_article(
                                self,
                                md_path=md_file,
                                post_metadata=post_metadata,
                            )
                            if verbose:
                                print(f"The post {md_file} uploads successful!")
                    else:
                        if verbose:
                            print(f"The post {md_file} is uploading...")
                        if filename_prefix in self.article_title_dict:
                            _update_article(
                                self,
                                md_path=md_file,
                                post_metadata=post_metadata,
                                last_update=last_update,
                            )
                        else:
                            _create_article(
                                self,
                                md_path=md_file,
                                post_metadata=post_metadata,
                            )
                        if verbose:
                            print(f"The post {md_file} uploads successful!")
                else:  # update
                    if filename_prefix in self.article_title_dict:
                        _update_article(
                            self,
                            md_path=md_file,
                            post_metadata=post_metadata,
                            last_update=last_update,
                        )
                        if verbose:
                            print(f"The post {md_file} updates successful!")
                    else:
                        if verbose:
                            print(
                                f'Warning: Could not find the post "{md_file}" in WordPress. '
                                f'Treating it as new content and uploading instead...'
                            )
                        _create_article(
                            self,
                            md_path=md_file,
                            post_metadata=post_metadata,
                        )
                        if verbose:
                            print(f"The post {md_file} uploads successful!")
                return

            except RuntimeError as e:
                # 检查是否为 429 错误
                if "429" in str(e) and self.rate_limiter:
                    retry_count += 1
                    if retry_count > max_retries:
                        raise RuntimeError(f"Max 429 retries exceeded for {md_file}")

                    should_continue = await self.rate_limiter.handle_429(retry_count)
                    if not should_continue:
                        raise
                else:
                    # 非 429 错误，直接抛出
                    raise
