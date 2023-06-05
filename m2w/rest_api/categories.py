#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: categories.py
# @Software: PyCharm

import httpx
import math
import asyncio


async def __categories_request(self, client: httpx.AsyncClient(), page_num: int):
    resp = await client.get(
        self.url + f"wp-json/wp/v2/categories?page={page_num}&per_page=30"
    )
    try:
        assert (
            resp.status_code == 200
        ), "Error when requiring category lists. Pleas try later!"
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError

    for categories in resp.json():
        self.categories_dict[categories["name"]] = int(categories["id"])


async def get_all_categories(self, verbose) -> None:
    """
    获取所有的类别信息
    """
    categories_num = httpx.get(
        self.url + "wp-json/wp/v2/tags?page=1&per_page=1"
    ).headers['x-wp-total']
    page_num = math.ceil(float(categories_num) / 30.0)
    async with httpx.AsyncClient() as client:
        task_list = []
        for num in range(1, page_num + 1):
            req = __categories_request(self, client, num)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
    if verbose:
        print("Get category lists complete!")


def create_category(self, category_name: str) -> int:
    """
    创建category
    @param self:
    @param category_name: 类别名
    @return: 创建category的id
    """
    try:
        resp = httpx.post(
            url=self.url + "wp-json/wp/v2/categories",
            headers=self.wp_header,
            json={"name": category_name},
        )
        assert (
            resp.status_code == 201
        ), f"Category created failed. Please try again! Messages: {resp.json()['message']}"
        self.categories_dict[category_name] = resp.json()['id']
        return resp.json()['id']
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
