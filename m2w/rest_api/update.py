#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 17:35
# @Author  : Suzuran
# @FileName: update.py
# @Software: PyCharm

from .categories import create_category
from .tags import create_tag
from .articles import normalize_title
from .utils import lookup_taxonomy_id, ensure_wp_success, DEFAULT_TIMEOUT
import frontmatter
import markdown
import os
import httpx
import time

try:
    from markdown_gfm_admonition import GfmAdmonitionExtension
    HAS_GFM_ADMONITION = True
except ImportError:
    HAS_GFM_ADMONITION = False

from m2w.math import MathExtension


def _update_article(self, md_path, post_metadata, last_update=False) -> None:
    """
    更新文章
    @param md_path: md文件路径
    @param post_metadata: 上传文件的元信息
    @return:
    """

    filename = os.path.basename(md_path)
    filename_prefix, filename_suffix = os.path.splitext(
        filename
    )
    filename_prefix = normalize_title(filename_prefix)

    try:
        assert filename_suffix == ".md", "Only files with suffix .md supported!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(md_path)

    # 2 检查是否需要删除文章（status: delete）
    if post_from_file.metadata.get("status") == "delete":
        _delete_article(self, md_path, filename_prefix)
        return

    # 3 markdown库导入内容
    extensions = ['markdown.extensions.fenced_code', 'tables', MathExtension()]
    if HAS_GFM_ADMONITION:
        extensions.append(GfmAdmonitionExtension())

    post_content_html = markdown.markdown(
        post_from_file.content, extensions=extensions
    )
    post_content_html = post_content_html.encode("utf-8")

    # 4 将本地post的元数据暂存到metadata中
    metadata_keys = post_metadata.keys()
    for key in metadata_keys:
        if (
            key in post_from_file.metadata
        ):  # 若md文件中没有元数据'category'，则无法调用post.metadata['category']
            post_metadata[key] = post_from_file.metadata[key]

    # 5 更新tag和category的id信息
    tags = []
    categories = []
    for tag in post_metadata["tag"]:
        tag_id = lookup_taxonomy_id(self.tags_dict, tag)
        if tag_id is None:
            tag_id = create_tag(self, tag)
        tags.append(tag_id)
    for category in post_metadata["category"]:
        category_id = lookup_taxonomy_id(self.categories_dict, category)
        if category_id is None:
            category_id = create_category(self, category)
        categories.append(category_id)

    # 6 构造上传的请求内容
    post_data = {
        "content": str(post_content_html, encoding="utf-8"),
        "categories": categories,
        "tags": tags,
    }

    # 7 支持修改文章状态
    if "status" in post_from_file.metadata:
        post_data["status"] = post_from_file.metadata["status"]

    # 8 支持 URL 别名修改
    if "slug" in post_from_file.metadata:
        post_data["slug"] = post_from_file.metadata["slug"]

    # 9 支持标题修改
    if "title" in post_from_file.metadata:
        post_data["title"] = post_from_file.metadata["title"]

    if last_update:
        post_data['date'] = time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.localtime(time.time()),
        )

    resp = httpx.post(
        url=self.url
        + f"wp-json/wp/v2/posts/{self.article_title_dict[filename_prefix]}",
        headers=self.wp_header,
        json=post_data,
        timeout=getattr(self, "timeout", DEFAULT_TIMEOUT),
    )
    ensure_wp_success(resp, f"File {md_path} updated")


def _delete_article(self, md_path, filename_prefix) -> None:
    """
    删除文章
    @param md_path: md文件路径
    @param filename_prefix: 标准化后的文件名前缀
    @return:
    """
    import os as os_module

    post_id = self.article_title_dict.get(filename_prefix)
    if post_id is None:
        print(f"Warning: Could not find post '{filename_prefix}' to delete.")
        return

    # 调用 WordPress REST API 删除文章
    resp = httpx.delete(
        url=self.url + f"wp-json/wp/v2/posts/{post_id}?force=true",
        headers=self.wp_header,
        timeout=getattr(self, "timeout", DEFAULT_TIMEOUT),
    )

    try:
        ensure_wp_success(resp, f"File {md_path} deleted")
        print(f"Delete article: {md_path}")

        # 从 article_title_dict 中移除
        self.article_title_dict.pop(filename_prefix, None)

        # 删除本地 markdown 文件
        if os_module.path.exists(md_path):
            os_module.remove(md_path)

    except Exception as e:
        print(f"Failed to delete article {md_path}: {e}")
        raise
