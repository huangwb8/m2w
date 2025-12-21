#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: categories.py
# @Software: PyCharm

import asyncio
import httpx
import math

from .utils import format_wp_error, register_taxonomy_alias
from .utils import DEFAULT_TIMEOUT


def _cache_category_aliases(store, payload) -> None:
    category_id = int(payload["id"])
    register_taxonomy_alias(store, category_id, payload.get("name"), payload.get("slug"))


async def __categories_request(self, client: httpx.AsyncClient(), page_num: int):
    resp = await client.get(
        self.url + f"wp-json/wp/v2/categories?page={page_num}&per_page=30"
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"Error when requiring category lists: {format_wp_error(resp)}"
        )

    for category in resp.json():
        _cache_category_aliases(self.categories_dict, category)


async def get_all_categories(self, verbose) -> None:
    """
    获取所有的类别信息
    """
    timeout = getattr(self, "timeout", DEFAULT_TIMEOUT)
    categories_num = httpx.get(
        self.url + "wp-json/wp/v2/categories?page=1&per_page=1",
        timeout=timeout,
    ).headers['x-wp-total']
    page_num = math.ceil(float(categories_num) / 30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
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
    resp = httpx.post(
        url=self.url + "wp-json/wp/v2/categories",
        headers=self.wp_header,
        json={"name": category_name},
        timeout=getattr(self, "timeout", DEFAULT_TIMEOUT),
    )
    if resp.status_code == 201:
        payload = resp.json()
        category_id = int(payload['id'])
        _cache_category_aliases(self.categories_dict, payload)
        register_taxonomy_alias(self.categories_dict, category_id, category_name)
        return category_id

    if resp.status_code == 400:
        try:
            payload = resp.json()
        except ValueError:
            payload = None
        if isinstance(payload, dict) and payload.get("code") == "term_exists":
            term_id = payload.get("data", {}).get("term_id")
            if term_id is not None:
                term_id = int(term_id)
                register_taxonomy_alias(self.categories_dict, term_id, category_name)
                return term_id

    raise RuntimeError(
        f"Category created failed: {format_wp_error(resp)}"
    )
