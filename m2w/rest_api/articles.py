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
    "’": "'",
    "‘": "'",
    "＇": "'",
    "“": "'",
    "”": "'",
    "＂": "'",
    "\"": "'",
    "–": "-",
    "—": "-",
    "‐": "-",
    "−": "-",
    "﹣": "-",
    "～": "~",
    "　": " ",  # full-width space
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


async def __article_title_request(self, client: httpx.AsyncClient(), page_num: int):
    resp = await client.get(
        self.url + f"wp-json/wp/v2/posts?page={page_num}&per_page=30"
    )
    try:
        assert (
            resp.status_code == 200
        ), "Error when requiring article lists. Pleas try later!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    for article in resp.json():
        self.article_title_dict[normalize_title(article["title"]["rendered"])] = article['id']


async def get_all_articles(self, verbose) -> None:
    """
    获取所有的文章信息
    """
    timeout = getattr(self, "timeout", DEFAULT_TIMEOUT)
    article_num = httpx.get(
        self.url + "wp-json/wp/v2/posts?page=1&per_page=1",
        timeout=timeout,
    ).headers[
        'x-wp-total'
    ]
    page_num = math.ceil(float(article_num) / 30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        task_list = []
        for num in range(1, page_num + 1):
            req = __article_title_request(self, client, num)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
    if verbose:
        print("Get article lists complete!")
