"""
Legacy entrypoint for Password mode helpers.

This module is kept for backward compatibility and simply re-exports the
implementation that now lives under ``m2w.password``.
"""

from m2w.password import find_files, md_detect, up_password

__all__ = ["find_files", "md_detect", "up_password"]
