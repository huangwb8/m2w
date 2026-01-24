#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 17:35
# @Author  : Suzuran
# @FileName: create.py
# @Software: PyCharm

from .tags import create_tag
from .categories import create_category
from .utils import lookup_taxonomy_id, ensure_wp_success, DEFAULT_TIMEOUT
import frontmatter
import markdown
import os
import httpx

try:
    from markdown_gfm_admonition import GfmAdmonitionExtension
    HAS_GFM_ADMONITION = True
except ImportError:
    HAS_GFM_ADMONITION = False

from m2w.math import MathExtension


def _create_article(self, md_path, post_metadata) -> None:
    """
    创建文章
    @param md_path: md文件路径
    @param post_metadata: 上传文件的元信息
    @return:
    """
    filename = os.path.basename(md_path)

    try:
        assert filename.split('.')[-1] == "md", "Only files with suffix .md supported!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(md_path)

    # 2 markdown库导入内容
    extensions = ['markdown.extensions.fenced_code', 'tables', MathExtension()]
    if HAS_GFM_ADMONITION:
        extensions.append(GfmAdmonitionExtension())

    post_content_html = markdown.markdown(
        post_from_file.content, extensions=extensions
    )
    post_content_html = post_content_html.encode("utf-8")

    # 3 将本地post的元数据暂存到metadata中
    metadata_keys = post_metadata.keys()
    for key in metadata_keys:
        if (
            key in post_from_file.metadata
        ):  # 若md文件中没有元数据'category'，则无法调用post.metadata['category']
            post_metadata[key] = post_from_file.metadata[key]

    # 4 更新tag和category的id信息
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

    # 5 确定标题：优先使用 frontmatter 中的 title
    title = post_from_file.metadata.get("title", filename.split(".md")[0])

    # 6 构造上传的请求内容
    post_data = {
        "title": title,
        "content": str(post_content_html, encoding="utf-8"),
        "status": post_metadata["status"],
        "comment_status": "open",
        "categories": categories,
        "tags": tags,
    }

    # 7 支持自定义 post_type（如 shuoshuo、page 等）
    if "post_type" in post_from_file.metadata:
        post_data["post_type"] = post_from_file.metadata["post_type"]

    # 8 支持 URL 别名设置
    if "slug" in post_from_file.metadata:
        post_data["slug"] = post_from_file.metadata["slug"]

    # 9 确定 API 端点：post_type 可能不同
    post_type = post_data.get("post_type", "post")
    if post_type == "post":
        endpoint = "wp-json/wp/v2/posts"
    elif post_type == "page":
        endpoint = "wp-json/wp/v2/pages"
    else:
        # 对于自定义 post_type（如 shuoshuo），尝试使用自定义文章类型端点
        endpoint = f"wp-json/wp/v2/{post_type}"

    resp = httpx.post(
        url=self.url + endpoint,
        headers=self.wp_header,
        json=post_data,
        timeout=getattr(self, "timeout", DEFAULT_TIMEOUT),
    )
    ensure_wp_success(resp, f"File {md_path} uploaded")
