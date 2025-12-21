#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 4:36
# @Author  : Suzuran
# @FileName: tags.py
# @Software: PyCharm

import asyncio
import httpx
import math

from .utils import format_wp_error, register_taxonomy_alias
from .utils import DEFAULT_TIMEOUT


def _cache_tag_aliases(store, payload) -> None:
    tag_id = int(payload["id"])
    register_taxonomy_alias(store, tag_id, payload.get("name"), payload.get("slug"))


async def __tags_request(self, client: httpx.AsyncClient(), page_num: int):
    resp = await client.get(
        self.url + f"wp-json/wp/v2/tags?page={page_num}&per_page=30"
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Error when requiring tag lists: {format_wp_error(resp)}")

    for tag in resp.json():
        _cache_tag_aliases(self.tags_dict, tag)


async def get_all_tags(self, verbose) -> None:
    """
    获取所有的标签信息
    """
    timeout = getattr(self, "timeout", DEFAULT_TIMEOUT)
    tags_num = httpx.get(
        self.url + "wp-json/wp/v2/tags?page=1&per_page=1",
        timeout=timeout,
    ).headers[
        'x-wp-total'
    ]
    page_num = math.ceil(float(tags_num) / 30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
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
    resp = httpx.post(
        url=self.url + "wp-json/wp/v2/tags",
        headers=self.wp_header,
        json={"name": tag_name},
        timeout=getattr(self, "timeout", DEFAULT_TIMEOUT),
    )
    if resp.status_code == 201:
        payload = resp.json()
        tag_id = int(payload['id'])
        _cache_tag_aliases(self.tags_dict, payload)
        register_taxonomy_alias(self.tags_dict, tag_id, tag_name)
        return tag_id

    if resp.status_code == 400:
        try:
            payload = resp.json()
        except ValueError:
            payload = None
        if isinstance(payload, dict) and payload.get("code") == "term_exists":
            term_id = payload.get("data", {}).get("term_id")
            if term_id is not None:
                term_id = int(term_id)
                register_taxonomy_alias(self.tags_dict, term_id, tag_name)
                return term_id

    raise RuntimeError(f"Tag created failed: {format_wp_error(resp)}")
