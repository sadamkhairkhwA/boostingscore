"""Signup email verification.

New accounts are created inactive and must confirm their email before they can
log in. This mirrors the email-change flow but activates a brand-new account.

IMPORTANT: email delivery must never prevent or roll back account creation.
Callers must save the User first; this module only sends mail and never raises.
"""
from __future__ import annotations

import logging
import os

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse

logger = logging.getLogger(__name__)

SIGNUP_SALT = "boostingscore.signup-verify"
SIGNUP_MAX_AGE = 60 * 60 * 24 * 3  # 3 days

FALLBACK_MSG = (
    "Account created — if you don't receive an email shortly, "
    "use Resend below or contact support."
)


def make_signup_token(user_id: int, email: str) -> str:
    return signing.dumps(
        {"uid": user_id, "email": (email or "").lower().strip()},
        salt=SIGNUP_SALT,
    )


def load_signup_token(token: str) -> dict:
    return signing.loads(token, salt=SIGNUP_SALT, max_age=SIGNUP_MAX_AGE)


def _using_console_email() -> bool:
    backend = (getattr(settings, "EMAIL_BACKEND", "") or "").lower()
    return "console" in backend or "locmem" in backend or "dummy" in backend


def _deliver_signup_email(subject: str, body: str, from_email: str, email: str) -> bool:
    """Attempt delivery. Returns True on success. Never raises."""
    try:
        sent = send_mail(subject, body, from_email, [email], fail_silently=False)
        return bool(sent)
    except Exception as exc:
        logger.warning("signup verification send failed: %s", exc)
        return False


def _absolute_verify_url(request, path: str) -> str:
    """Build an absolute URL without letting a bad Host header abort signup."""
    try:
        return request.build_absolute_uri(path)
    except Exception as exc:
        logger.warning("build_absolute_uri failed (%s); using configured origin", exc)
    origins = getattr(settings, "CSRF_TRUSTED_ORIGINS", None) or []
    base = (origins[0] if origins else "").rstrip("/")
    if not base:
        base = (os.environ.get("PUBLIC_BASE_URL") or "https://boostingscore.com").rstrip("/")
    return f"{base}{path}"


def send_signup_verification(request, user) -> tuple[bool, str, str]:
    """Queue/send a verification link for an already-saved (inactive) account.

    Always returns ``(True, message, verify_url_or_empty)`` so the signup view
    can show the check-email page. Failures are logged only.

    In production, delivery is scheduled with ``transaction.on_commit`` so it
    cannot run (or hang) inside the same DB transaction as ``user.save()`` —
    a killed/timed-out email request must never roll the User row back.
    """
    email = (user.email or "").lower().strip()
    try:
        token = make_signup_token(user.id, email)
        path = reverse("signup_verify", kwargs={"token": token})
        verify_url = _absolute_verify_url(request, path)
    except Exception as exc:
        logger.warning("signup verification token/url failed: %s", exc)
        return True, FALLBACK_MSG, ""

    show_link = _using_console_email() or settings.DEBUG

    subject = "Confirm your email — BoostingScore"
    body = (
        f"Welcome to BoostingScore!\n\n"
        f"Confirm your email to activate your account by opening this link "
        f"(valid for 3 days):\n"
        f"{verify_url}\n\n"
        f"If you did not create this account, you can ignore this email.\n\n"
        f"— BoostingScore\n"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@boostingscore.com")

    if show_link:
        # Local/dev: send now so the console backend prints the link immediately.
        ok = _deliver_signup_email(subject, body, from_email, email)
        return (
            True,
            (
                f"Local/dev mode: email is not delivered to an inbox "
                f"(console backend). Use the button below to verify {email}."
                if ok or _using_console_email()
                else FALLBACK_MSG
            ),
            verify_url,
        )

    # Production: only send AFTER the surrounding transaction commits, so a
    # Resend/SMTP hang or exception cannot roll back the User row.
    def _send_after_commit():
        ok = _deliver_signup_email(subject, body, from_email, email)
        if not ok:
            logger.warning(
                "signup verification email not delivered for user_id=%s email=%s",
                user.id,
                email,
            )

    try:
        transaction.on_commit(_send_after_commit)
    except Exception as exc:
        # Extremely defensive: if on_commit itself fails, try a best-effort send
        # but still never raise to the signup view.
        logger.warning("signup on_commit schedule failed: %s", exc)
        _deliver_signup_email(subject, body, from_email, email)

    return (
        True,
        f"We sent a verification link to {email}. Open it to activate your account.",
        "",
    )
