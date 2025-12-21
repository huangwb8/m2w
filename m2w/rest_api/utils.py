#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""WordPress REST API utility helpers."""

import httpx
import unicodedata
from typing import Dict, Optional


# Use a generous default timeout because some WordPress hosts respond slowly.
DEFAULT_TIMEOUT = httpx.Timeout(30.0)


def format_wp_error(response) -> str:
    """Return a readable error string extracted from a WordPress REST response."""
    try:
        payload = response.json()
    except ValueError:
        payload = None

    details = []
    if isinstance(payload, dict):
        message = payload.get("message")
        code = payload.get("code")
        data = payload.get("data")
        if isinstance(message, str) and message.strip():
            details.append(message.strip())
        elif code:
            details.append(str(code))
        if isinstance(data, dict):
            status = data.get("status")
            term_id = data.get("term_id")
            extra = []
            if status:
                extra.append(f"status={status}")
            if term_id:
                extra.append(f"term_id={term_id}")
            if extra:
                details.append(", ".join(extra))
    elif isinstance(payload, list):
        details.append(str(payload))
    else:
        text = response.text.strip()
        if text:
            details.append(text)

    if not details:
        details.append("WordPress response contained no details.")
    return f"HTTP {response.status_code}: {'; '.join(details)}"


def normalize_taxonomy_key(value: Optional[str]) -> Optional[str]:
    """Normalize taxonomy name/slug for alias mapping."""
    if not isinstance(value, str):
        return None
    normalized = unicodedata.normalize("NFKC", value).strip()
    if not normalized:
        return None
    return normalized.casefold()


def register_taxonomy_alias(store: Dict[str, int], term_id: int, *aliases: Optional[str]) -> None:
    """Register multiple aliases pointing to the same taxonomy id."""
    for alias in aliases:
        normalized = normalize_taxonomy_key(alias)
        if normalized:
            store[normalized] = term_id


def lookup_taxonomy_id(store: Dict[str, int], name: str) -> Optional[int]:
    """Return cached taxonomy id that matches the provided name/slug."""
    normalized = normalize_taxonomy_key(name)
    if not normalized:
        return None
    return store.get(normalized)


def ensure_wp_success(response, action: str) -> None:
    """Raise RuntimeError when the HTTP response indicates failure."""
    if not (200 <= response.status_code < 300):
        raise RuntimeError(f"{action} failed: {format_wp_error(response)}")
