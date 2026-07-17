"""Signup email verification.

New accounts are created inactive and must confirm their email before they can
log in. This mirrors the email-change flow but activates a brand-new account.
"""
from __future__ import annotations

import logging

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


def send_signup_verification(request, user) -> tuple[bool, str]:
    """Email a verification link to a freshly-created (inactive) account.

    Returns (ok, message_for_user). On dev/misconfigured mail the link is
    surfaced in the message so local signups can still be completed.
    """
    email = (user.email or "").lower().strip()
    token = make_signup_token(user.id, email)
    path = reverse("signup_verify", kwargs={"token": token})
    verify_url = request.build_absolute_uri(path)

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

    try:
        sent = send_mail(subject, body, from_email, [email], fail_silently=False)
        if sent:
            return True, f"We sent a verification link to {email}. Open it to activate your account."
    except Exception as exc:
        logger.warning("signup verification send failed: %s", exc)

    if settings.DEBUG:
        return True, (
            f"Verification email could not be delivered (check EMAIL settings). "
            f"Dev link: {verify_url}"
        )
    return False, (
        "We created your account but could not send the verification email. "
        "Use the resend button below or try again later."
    )
