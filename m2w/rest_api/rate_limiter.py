#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Rate limiter for WordPress REST API requests."""

import asyncio
from typing import Optional


class RateLimiter:
    """
    速率限制器，支持固定延迟、批次处理和 429 指数退避。

    用于控制上传请求的频率，避免触发 WordPress 服务器的速率限制。
    """

    def __init__(
        self,
        request_delay: float = 1.0,
        batch_size: int = 10,
        batch_delay: float = 5.0,
        max_429_retries: int = 5,
        initial_backoff: float = 2.0,
        backoff_multiplier: float = 2.0,
        verbose: bool = True,
    ):
        """
        初始化速率限制器。

        Args:
            request_delay: 每个请求之间的延迟时间（秒）
            batch_size: 每批处理的文件数量
            batch_delay: 批次之间的延迟时间（秒）
            max_429_retries: 遇到 429 错误时的最大重试次数
            initial_backoff: 指数退避的初始延迟时间（秒）
            backoff_multiplier: 每次退避的倍增系数
            verbose: 是否输出详细日志
        """
        self.request_delay = request_delay
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.max_429_retries = max_429_retries
        self.initial_backoff = initial_backoff
        self.backoff_multiplier = backoff_multiplier
        self.verbose = verbose

    async def wait_before_request(self, batch_position: int) -> None:
        """
        在发送请求前等待适当的时间。

        Args:
            batch_position: 当前文件在批次中的位置（从 0 开始）
        """
        # 不是批次第一个请求时，等待 request_delay
        if batch_position > 0:
            if self.verbose:
                print(f"  Waiting {self.request_delay}s before next request...")
            await asyncio.sleep(self.request_delay)

    async def handle_429(self, retry_count: int) -> bool:
        """
        处理 HTTP 429 错误，使用指数退避策略。

        Args:
            retry_count: 当前重试次数（从 1 开始）

        Returns:
            bool: 是否应该继续重试
        """
        if retry_count > self.max_429_retries:
            return False

        # 计算退避时间：initial_backoff * (backoff_multiplier ^ (retry_count - 1))
        backoff_time = self.initial_backoff * (
            self.backoff_multiplier ** (retry_count - 1)
        )

        if self.verbose:
            print(
                f"  HTTP 429 detected. Retrying ({retry_count}/{self.max_429_retries}) "
                f"after {backoff_time}s backoff..."
            )

        await asyncio.sleep(backoff_time)
        return True

    def is_batch_boundary(self, position: int, batch_size: Optional[int] = None) -> bool:
        """
        判断当前位置是否为批次边界。

        Args:
            position: 当前文件在批次中的位置
            batch_size: 批次大小（默认使用 self.batch_size）

        Returns:
            bool: 是否到达批次边界
        """
        size = batch_size or self.batch_size
        return position > 0 and position % size == 0
