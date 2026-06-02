"""Resolve OpenAI API key from environment or ``.env`` (including legacy formats)."""

from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings


def _parse_env_value(rest: str) -> str:
    rest = (rest or "").strip()
    if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in "\"'":
        return rest[1:-1].strip()
    return rest


def resolve_openai_api_key() -> str:
    env_val = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if env_val:
        return env_val

    path = Path(settings.BASE_DIR) / ".env"
    if not path.is_file():
        return ""

    text = path.read_text(encoding="utf-8")

    # If `.env` contains multiple `OPENAI_API_KEY=` lines, the last one wins.
    last_key = ""
    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        key, sep, rest = raw.partition("=")
        if sep and key.strip().upper() == "OPENAI_API_KEY":
            last_key = _parse_env_value(rest)

    if last_key:
        return last_key

    # Legacy: a lone `sk-...` line with no `KEY=` prefix (older `.env` layouts).
    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if "=" in raw:
            continue
        if raw.startswith("sk-"):
            return raw

    return ""
