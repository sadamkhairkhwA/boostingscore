"""Build Django DATABASES from DATABASE_URL (e.g. Supabase PostgreSQL)."""
import os
from urllib.parse import parse_qs, unquote, urlparse


def database_config_from_url(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise ValueError("DATABASE_URL must use postgres:// or postgresql://")

    path = (parsed.path or "").lstrip("/")
    name, _, _ = path.partition("/")
    if not name:
        raise ValueError("DATABASE_URL must include a database name")

    password = unquote(parsed.password) if parsed.password else ""
    user = unquote(parsed.username) if parsed.username else ""

    options = {}
    qs = parse_qs(parsed.query)
    for key in ("sslmode", "connect_timeout", "options"):
        if key in qs and qs[key]:
            options[key] = qs[key][0]
    if "sslmode" not in options:
        options["sslmode"] = "require"

    port = parsed.port or 5432
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": user,
        "PASSWORD": password,
        "HOST": parsed.hostname or "",
        "PORT": str(port),
        "OPTIONS": options,
        "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
    }
