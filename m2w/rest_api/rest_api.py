#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 0:27
# @Author  : Suzuran
# @FileName: rest_api.py
# @Software: PyCharm
import os
import asyncio
import base64

from .articles import get_all_articles
from .tags import get_all_tags
from .categories import get_all_categories
from .update import _update_article
from .create import _create_article


class RestApi:
    def __init__(self, url: str, wp_username=None, wp_password=None):
        self.url = url if url.endswith("/") else url + "/"
        self.wp_header = {
            "Authorization": "Basic "
            + base64.b64encode(f"{wp_username}:{wp_password}".encode()).decode("utf-8")
        }
        self.article_title_dict = {}
        self.categories_dict = {}
        self.tags_dict = {}

    async def upload_article(
        self, md_message=None, post_metadata=None, verbose=True, force_upload=False
    ):
        """
        自动判断更新还是创建
        @param verbose: 是否输出控制台信息
        @param force_upload: 是否启用强制上传
        @param post_metadata: 上传文件的元信息
        @param md_message: 需要更新的md文件路径信息
        @return:
        """

        # 更新现有文章信息
        articles_async = asyncio.create_task(get_all_articles(self))
        tags_async = asyncio.create_task(get_all_tags(self))
        categories_async = asyncio.create_task(get_all_categories(self))

        await categories_async
        await tags_async
        await articles_async

        md_create = md_message['new']
        md_update = md_message['legacy']

        None if not verbose else print(
            "You don't want a force uploading. The existence of the post would be checked."
        ) if not force_upload else print("You want a force uploading? Great!")

        for new_md in md_create:
            if not force_upload:
                if (
                    os.path.basename(new_md).strip(".md")
                    in self.article_title_dict.keys()
                ):
                    if verbose:
                        print(
                            f'Warning: The post {new_md} is existed in your WordPress site. Ignore uploading!'
                        )
                else:
                    if verbose:
                        print(
                            f'The post {new_md} is exactly a new one in your WordPress site! Try uploading...'
                        )
                    _create_article(
                        self,
                        md_path=new_md,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload,
                    )
                    if verbose:
                        print(f"The post {new_md} uploads successful\n")
            else:
                print(f"The post {new_md} is updating")
                if (
                    os.path.basename(new_md).strip(".md")
                    in self.article_title_dict.keys()
                ):
                    _update_article(
                        self,
                        md_path=new_md,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload,
                    )
                else:
                    _create_article(
                        self,
                        md_path=new_md,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload,
                    )
                print(f"The post {new_md} uploads successful\n")
        for legacy_md in md_update:
            if (
                os.path.basename(legacy_md).strip(".md")
                in self.article_title_dict.keys()
            ):
                _update_article(
                    self,
                    md_path=legacy_md,
                    post_metadata=post_metadata,
                    verbose=verbose,
                    force_upload=force_upload,
                )
                if verbose:
                    print(f"The post {legacy_md} updates successful\n")
            else:
                if verbose:
                    print(
                        'FAILURE to find the post. Please check your User Configuration and the title in your '
                        'WordPress.'
                    )
