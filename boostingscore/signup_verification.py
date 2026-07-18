"""Signup email verification.

New accounts are created inactive and must confirm their email before they can
log in. This mirrors the email-change flow but activates a brand-new account.
"""
from __future__ import annotations

import logging
import threading

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse

logger = logging.getLogger(__name__)

SIGNUP_SALT = "boostingscore.signup-verify"
SIGNUP_MAX_AGE = 60 * 60 * 24 * 3  # 3 days


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


def _deliver_signup_email(subject: str, body: str, from_email: str, email: str) -> None:
    try:
        send_mail(subject, body, from_email, [email], fail_silently=False)
    except Exception as exc:
        logger.warning("signup verification send failed: %s", exc)


def send_signup_verification(request, user) -> tuple[bool, str, str]:
    """Email a verification link to a freshly-created (inactive) account.

    Returns ``(ok, message_for_user, verify_url_for_ui)``.
    ``verify_url_for_ui`` is only set in console/DEBUG mode so the check-email
    page can show a clickable link (nothing reaches a real inbox locally).
    In production the link goes only in the email; signup always proceeds to
    the check-email page even if delivery fails (errors are logged).
    """
    email = (user.email or "").lower().strip()
    token = make_signup_token(user.id, email)
    path = reverse("signup_verify", kwargs={"token": token})
    verify_url = request.build_absolute_uri(path)
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
        # Local/dev: send synchronously so console backend prints the link now.
        try:
            send_mail(subject, body, from_email, [email], fail_silently=False)
        except Exception as exc:
            logger.warning("signup verification send failed: %s", exc)
        return (
            True,
            (
                f"Local/dev mode: email is not delivered to an inbox "
                f"(console backend). Use the button below to verify "
                f"{email}."
            ),
            verify_url,
        )

    # Production: never block the signup HTTP request on SMTP/API latency.
    # Railway Hobby blocks outbound SMTP, so a sync send can hang until timeout.
    threading.Thread(
        target=_deliver_signup_email,
        args=(subject, body, from_email, email),
        daemon=True,
        name="signup-verify-email",
    ).start()
    return (
        True,
        f"We sent a verification link to {email}. Open it to activate your account.",
        "",
    )
