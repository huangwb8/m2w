#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: tags.py
# @Software: PyCharm
import re

import httpx
import math
import asyncio


async def __tags_request(self, client: httpx.AsyncClient(), page_num: int):
    resp = await client.get(
        self.url + f"wp-json/wp/v2/tags?page={page_num}&per_page=30"
    )
    try:
        assert (
            resp.status_code == 200
        ), "Error when requiring tag lists. Pleas try later!"
    except AssertionError as e:
        print("Reminder from Bensz(https://blognas.hwb0307.com) : " + str(e))
        raise AssertionError

    for tags in resp.json():
        self.tags_dict[tags['name']] = tags['id']


async def get_all_tags(self, verbose) -> None:
    """
    获取所有的标签信息
    """
    tags_num = httpx.get(self.url + "wp-json/wp/v2/tags?page=1&per_page=1").headers[
        'x-wp-total'
    ]
    page_num = math.ceil(float(tags_num) / 30.0)
    async with httpx.AsyncClient() as client:
        task_list = []
        for num in range(1, page_num + 1):
            req = __tags_request(self, client, num)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
    if verbose:
        print("Get tag lists complete!")


def create_tag(self, tag_name: str) -> int:
    """
    创建tag
    @param self:
    @param tag_name: 标签名
    @return: 创建tag的id
    """
    try:
        resp = httpx.post(
            url=self.url + "wp-json/wp/v2/tags",
            headers=self.wp_header,
            json={"name": tag_name},
        )
        assert (
            resp.status_code == 201
        ), f"Tag created failed. Please try again! Messages:{resp.json()['message']}"
        self.tags_dict[tag_name] = resp.json()["id"]
        return resp.json()['id']
    except AssertionError as e:
        print("Reminder from m2w: " + str(e))
        raise AssertionError
