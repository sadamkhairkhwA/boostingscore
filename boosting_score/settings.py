from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "True") == "True"
# Hard safety net: never run with DEBUG=True on Railway, even if the DEBUG env
# var is missing or misset. DEBUG also gates the on-page signup dev code.
if any(
    os.environ.get(var)
    for var in ("RAILWAY_ENVIRONMENT", "RAILWAY_PROJECT_ID", "RAILWAY_PUBLIC_DOMAIN")
):
    DEBUG = False
# Comma-separated hostnames (no scheme), e.g. localhost,127.0.0.1,boostingscore.com
_allowed = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]
# Railway injects these; include them so a missing ALLOWED_HOSTS env doesn't brick the site.
for _extra in (
    os.environ.get("RAILWAY_PUBLIC_DOMAIN", ""),
    os.environ.get("RAILWAY_STATIC_URL", ""),
):
    _host = (_extra or "").strip().removeprefix("https://").removeprefix("http://").split("/")[0]
    if _host and _host not in _allowed:
        _allowed.append(_host)
ALLOWED_HOSTS = _allowed or ["localhost", "127.0.0.1"]
# Comma-separated origins, e.g. https://app.example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://boostingscore.com,https://www.boostingscore.com,"
        "https://boostingscore-production.up.railway.app",
    ).split(",")
    if origin.strip()
]
# TEMP: confirm Railway env is applied — remove once CSRF is verified in prod.
print(f"[startup] CSRF_TRUSTED_ORIGINS={CSRF_TRUSTED_ORIGINS!r}", flush=True)
print(f"[startup] ALLOWED_HOSTS={ALLOWED_HOSTS!r}", flush=True)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "vocabulary.apps.VocabularyConfig",
    "reading",
    "writing",
    "practice_test.apps.PracticeTestConfig",
    "listening.apps.ListeningConfig",
    "speaking.apps.SpeakingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # After auth so staff users can be exempted from the maintenance page.
    "boostingscore.maintenance_middleware.MaintenanceModeMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "boostingscore.feedback_middleware.FeedbackWidgetMiddleware",
]

ROOT_URLCONF = "boosting_score.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "boosting_score.context_processors.streak_context",
            ],
        },
    },
]

WSGI_APPLICATION = "boosting_score.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    )
}

# SQLite locks the entire database file on every write. Under multiple gunicorn
# workers (as on Railway) concurrent writes — e.g. session saves on every
# request — surface as "database is locked" / SessionInterrupted. Giving writers
# up to 30s to wait for the lock (instead of failing instantly) plus WAL mode
# (enabled in practice_test.apps.ready, so reads don't block the writer) makes
# SQLite safe for this level of concurrency. For heavy traffic, set DATABASE_URL
# to a Postgres instance and these options are simply ignored.
if DATABASES["default"].get("ENGINE", "").endswith("sqlite3"):
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"]["timeout"] = 30

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Manifest hashing requires collectstatic; plain storage in DEBUG avoids missing CSS in local dev.
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Public base URL for large media gitignored from the repo (speaking tips/videos,
# listening_audio). Example: https://pub-xxxx.r2.dev or https://media.example.com
# Leave empty/unset for local development — files are served from static/ as usual.
MEDIA_CDN_URL = (os.environ.get("MEDIA_CDN_URL", "") or "").strip().rstrip("/")

OPENAI_API_KEY = (os.environ.get("OPENAI_API_KEY", "") or "").strip()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "").strip()

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Email — console in local/dev; set RESEND_API_KEY in production.
# Railway Free/Trial/Hobby blocks outbound SMTP (ports 25/465/587), which caused
# "[Errno 110] Connection timed out". Resend's HTTPS API (port 443) is not blocked.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587") or 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
# Fail SMTP/API attempts quickly so signup never hangs on a blocked port.
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "8") or 8)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@boostingscore.com")
RESEND_API_KEY = (os.environ.get("RESEND_API_KEY", "") or "").strip()

_email_backend_env = (os.environ.get("EMAIL_BACKEND") or "").strip()
# RESEND_API_KEY always wins over a leftover EMAIL_BACKEND=smtp.* env var —
# otherwise Railway keeps dialing blocked SMTP ports and signup workers time out.
if RESEND_API_KEY:
    EMAIL_BACKEND = "boostingscore.email_backends.ResendAPIEmailBackend"
elif _email_backend_env:
    EMAIL_BACKEND = _email_backend_env
elif EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    # Local development: emails print to the runserver console.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
