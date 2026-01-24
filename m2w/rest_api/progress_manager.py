#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Progress manager for resumable uploads."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class ProgressManager:
    """
    进度管理器，支持断点续传。

    保存上传进度到文件，支持从中断点恢复。
    """

    def __init__(
        self, progress_file: str, enabled: bool = True, verbose: bool = True
    ):
        """
        初始化进度管理器。

        Args:
            progress_file: 进度文件路径
            enabled: 是否启用进度管理
            verbose: 是否输出详细日志
        """
        self.progress_file = progress_file
        self.enabled = enabled
        self.verbose = verbose
        self._data: Dict[str, Any] = {}

        if self.enabled:
            self._load()

    def _load(self) -> None:
        """加载进度文件。"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                if self.verbose:
                    completed = len(self._data.get("completed", []))
                    total = self._data.get("total", 0)
                    current = self._data.get("current_index", 0)
                    print(
                        f"Loaded progress: {completed}/{total} completed, "
                        f"resuming from index {current}"
                    )
            except (json.JSONDecodeError, IOError) as e:
                if self.verbose:
                    print(f"Warning: Failed to load progress file: {e}. Starting fresh.")
                self._data = {}
        else:
            self._data = {}

    def load(self) -> Dict[str, Any]:
        """
        获取进度数据。

        Returns:
            进度数据字典
        """
        return self._data

    def save(
        self,
        total: int,
        completed: List[str],
        failed: List[Dict[str, str]],
        current_index: int,
    ) -> None:
        """
        保存当前进度。

        Args:
            total: 总文件数
            completed: 已完成的文件路径列表
            failed: 失败的文件列表（包含文件路径和错误信息）
            current_index: 当前处理到的索引
        """
        if not self.enabled:
            return

        self._data.update(
            {
                "timestamp": datetime.now().isoformat(),
                "total": total,
                "completed": completed,
                "failed": failed,
                "current_index": current_index,
            }
        )

        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)

            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)

            if self.verbose:
                print(f"Progress saved: {len(completed)}/{total} completed")
        except IOError as e:
            if self.verbose:
                print(f"Warning: Failed to save progress: {e}")

    def mark_completed(self, file_path: str) -> None:
        """
        标记文件已完成。

        Args:
            file_path: 文件路径
        """
        if not self.enabled:
            return

        completed = self._data.get("completed", [])
        if file_path not in completed:
            completed.append(file_path)
        self._data["completed"] = completed

    def mark_failed(self, file_path: str, error: str) -> None:
        """
        标记文件失败。

        Args:
            file_path: 文件路径
            error: 错误信息
        """
        if not self.enabled:
            return

        failed = self._data.get("failed", [])
        failed.append(
            {
                "file": file_path,
                "error": error,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self._data["failed"] = failed

    def should_skip(self, file_path: str) -> bool:
        """
        判断文件是否已成功上传（用于断点续传）。

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否应该跳过该文件
        """
        if not self.enabled:
            return False
        return file_path in self._data.get("completed", [])

    def get_resume_index(self) -> int:
        """
        获取断点续传的起始索引。

        Returns:
            int: 起始索引
        """
        if not self.enabled:
            return 0
        return self._data.get("current_index", 0)

    def clear(self) -> None:
        """清空进度文件（全部成功完成后调用）。"""
        if not self.enabled:
            return

        if os.path.exists(self.progress_file):
            try:
                os.remove(self.progress_file)
                if self.verbose:
                    print("Progress cleared: All uploads completed successfully!")
            except IOError as e:
                if self.verbose:
                    print(f"Warning: Failed to clear progress file: {e}")
