#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: articles.py
# @Software: PyCharm

import httpx
import math
import asyncio
from html import unescape
import unicodedata
import re
from .utils import DEFAULT_TIMEOUT


_TITLE_TRANS_TABLE = str.maketrans({
    "\u2019": "'",
    "\u2018": "'",
    "\uff07": "'",
    "\u201c": "'",
    "\u201d": "'",
    "\uff42": "'",
    "\"": "'",
    "\u2013": "-",
    "\u2014": "-",
    "\u2010": "-",
    "\u2212": "-",
    "\ufe63": "-",
    "\uff5e": "~",
    "\u3000": " ",  # full-width space
    "\xa0": " ",
})


def normalize_title(raw_title):
    """标准化文章标题，移除空白并解码 HTML 实体。"""
    if not isinstance(raw_title, str):
        return raw_title
    text = unescape(raw_title)
    text = unicodedata.normalize('NFKC', text)
    text = text.translate(_TITLE_TRANS_TABLE)
    text = re.sub(r'-{2,}', '-', text)
    text = re.sub(r"'+", "'", text)
    text = ' '.join(text.split())
    return text.strip()


async def __article_title_request(self, client, page_num: int, endpoint: str):
    """获取文章列表的内部函数"""
    resp = await client.get(
        self.url + f"{endpoint}?page={page_num}&per_page=30"
    )
    try:
        assert (
            resp.status_code == 200
        ), f"Error when requiring {endpoint} lists. Please try later!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    for article in resp.json():
        self.article_title_dict[normalize_title(article["title"]["rendered"])] = article['id']


async def _get_articles_by_type(self, verbose, post_type: str) -> None:
    """
    根据文章类型获取文章列表

    Args:
        post_type: 文章类型，如 "post"、"page"、"shuoshuo" 等
    """
    timeout = getattr(self, "timeout", DEFAULT_TIMEOUT)

    # 根据 post_type 确定正确的 API 端点
    if post_type == "post":
        endpoint = "wp-json/wp/v2/posts"
    elif post_type == "page":
        endpoint = "wp-json/wp/v2/pages"
    else:
        # 对于自定义 post_type（如 shuoshuo）
        endpoint = f"wp-json/wp/v2/{post_type}"

    # 获取文章总数
    try:
        headers = httpx.get(
            self.url + f"{endpoint}?page=1&per_page=1",
            timeout=timeout,
        ).headers
        article_num = headers.get('x-wp-total', '0')
    except Exception as e:
        if verbose:
            print(f"Warning: Could not get {post_type} count: {e}")
        article_num = '0'

    page_num = math.ceil(float(article_num) / 30.0) if float(article_num) > 0 else 0

    if page_num > 0:
        async with httpx.AsyncClient(timeout=timeout) as client:
            task_list = []
            for num in range(1, page_num + 1):
                req = __article_title_request(self, client, num, endpoint)
                task = asyncio.create_task(req)
                task_list.append(task)
            await asyncio.gather(*task_list)


async def get_all_articles(self, verbose) -> None:
    """
    获取所有的文章信息（包括 posts 和 pages）
    """
    # 获取普通文章
    await _get_articles_by_type(self, verbose, post_type="post")

    # 获取页面
    await _get_articles_by_type(self, verbose, post_type="page")

    if verbose:
        print("Get article lists complete!")
