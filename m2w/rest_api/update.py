#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 17:35
# @Author  : Suzuran
# @FileName: update.py
# @Software: PyCharm
from markdown_gfm_admonition import GfmAdmonitionExtension

from .categories import create_category
from .tags import create_tag
import frontmatter
import markdown
import os
import httpx
import time
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

    try:
        assert filename_suffix == ".md", "Only files with suffix .md supported!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(md_path)

    # 2 markdown库导入内容
    post_content_html = markdown.markdown(
        post_from_file.content,
        extensions=['markdown.extensions.fenced_code', MathExtension(), 'tables', GfmAdmonitionExtension()]
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
        if tag in self.tags_dict.keys():
            tags.append(self.tags_dict[tag])
        else:
            tags.append(create_tag(self, tag))
    for category in post_metadata["category"]:
        if category in self.categories_dict.keys():
            categories.append(self.categories_dict[category])
        else:
            categories.append(create_category(self, category))

    # 5 构造上传的请求内容
    post_data = {
        "content": str(post_content_html, encoding="utf-8"),
        "categories": categories,
        "tags": tags,
    }

    if last_update:
        post_data['date'] = (
            time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time())),
        )

    resp = httpx.post(
        # url=self.url
        # + f"wp-json/wp/v2/posts/{self.article_title_dict[os.path.basename(md_path).strip('.md')]}",
        url=self.url
            + f"wp-json/wp/v2/posts/{self.article_title_dict[filename_prefix]}",
        headers=self.wp_header,
        json=post_data,
    )
    try:
        assert (
                resp.status_code == 200
        ), f"File {md_path} updated failed. Please try again!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError
