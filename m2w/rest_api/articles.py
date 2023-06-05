#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: articles.py
# @Software: PyCharm

import httpx
import math
import asyncio


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
        self.article_title_dict[article["title"]["rendered"]] = article['id']


async def get_all_articles(self, verbose) -> None:
    """
    获取所有的文章信息
    """
    article_num = httpx.get(self.url + "wp-json/wp/v2/posts?page=1&per_page=1").headers[
        'x-wp-total'
    ]
    page_num = math.ceil(float(article_num) / 30.0)
    async with httpx.AsyncClient() as client:
        task_list = []
        for num in range(1, page_num + 1):
            req = __article_title_request(self, client, num)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
    if verbose:
        print("Get article lists complete!")
