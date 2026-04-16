"""Resolve OPENAI_API_KEY from the process environment or project root `.env`."""
from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings


def resolve_openai_api_key() -> str:
    """Return trimmed API key, or empty string.

    Order:
    1. ``OPENAI_API_KEY`` in the process environment
    2. In ``BASE_DIR/.env``: a line ``OPENAI_API_KEY=...`` (optional ``export `` prefix;
       value may be quoted)
    3. Legacy: first non-comment, non-empty line that contains no ``=`` (raw key only)
    4. ``OPENAI_API_KEY`` on Django ``settings`` (optional explicit override in
       ``settings.py``, e.g. when not using env files)
    """
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if api_key:
        return api_key

    dotenv_path = Path(settings.BASE_DIR) / ".env"
    if not dotenv_path.is_file():
        sk = getattr(settings, "OPENAI_API_KEY", None)
        if sk is not None and str(sk).strip():
            return str(sk).strip()
        return ""

    legacy_raw: str | None = None
    for raw in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" in line:
            key, _, val = line.partition("=")
            if key.strip() == "OPENAI_API_KEY":
                return val.strip().strip('"').strip("'")
        elif legacy_raw is None:
            legacy_raw = line

    if legacy_raw:
        return legacy_raw

    sk = getattr(settings, "OPENAI_API_KEY", None)
    if sk is not None and str(sk).strip():
        return str(sk).strip()

    return ""
