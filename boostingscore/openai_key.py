"""Resolve OpenAI API key from environment or ``.env`` (including legacy formats)."""

from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings


def resolve_openai_api_key() -> str:
    env_val = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if env_val:
        return env_val

    path = Path(settings.BASE_DIR) / ".env"
    if not path.is_file():
        return ""

    text = path.read_text(encoding="utf-8")

    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        key, sep, rest = raw.partition("=")
        if sep and key.strip().upper() == "OPENAI_API_KEY":
            rest = rest.strip()
            if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in "\"'":
                return rest[1:-1]
            return rest

    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        return raw

    return ""
