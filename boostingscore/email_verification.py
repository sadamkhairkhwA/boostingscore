"""Email change verification helpers.

There was no previous verification flow — this module is the verify path used
when a logged-in user requests a new email from their Profile page.
"""
from __future__ import annotations

import logging

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)

EMAIL_CHANGE_SALT = "boostingscore.email-change"
EMAIL_CHANGE_MAX_AGE = 60 * 60 * 24  # 24 hours


def make_email_change_token(user_id: int, new_email: str) -> str:
    return signing.dumps(
        {"uid": user_id, "email": new_email.lower().strip()},
        salt=EMAIL_CHANGE_SALT,
    )


def load_email_change_token(token: str) -> dict:
    return signing.loads(token, salt=EMAIL_CHANGE_SALT, max_age=EMAIL_CHANGE_MAX_AGE)


def send_email_change_verification(request, user, new_email: str) -> tuple[bool, str]:
    """Save pending email, email a verify link. Returns (ok, message_for_user)."""
    from vocabulary.models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=user)
    new_email = new_email.lower().strip()
    profile.pending_email = new_email
    profile.pending_email_sent_at = timezone.now()
    profile.save(update_fields=["pending_email", "pending_email_sent_at"])

    token = make_email_change_token(user.id, new_email)
    path = reverse("profile_verify_email", kwargs={"token": token})
    verify_url = request.build_absolute_uri(path)

    subject = "Confirm your new email — BoostingScore"
    body = (
        f"Hi{' ' + user.first_name if user.first_name else ''},\n\n"
        f"You asked to change your BoostingScore email to {new_email}.\n\n"
        f"Confirm the change by opening this link (valid for 24 hours):\n"
        f"{verify_url}\n\n"
        f"If you did not request this, you can ignore this email. "
        f"Your current email stays the same until you confirm.\n\n"
        f"— BoostingScore\n"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@boostingscore.com")
    try:
        sent = send_mail(subject, body, from_email, [new_email], fail_silently=False)
        if sent:
            return True, f"We sent a confirmation link to {new_email}. Open it to finish the change."
    except Exception as exc:
        logger.warning("email change send failed: %s", exc)

    # Dev / misconfigured mail: still keep pending state; surface the link in the UI message.
    if settings.DEBUG:
        return True, (
            f"Confirmation email could not be delivered (check EMAIL settings). "
            f"Dev link: {verify_url}"
        )
    return False, (
        "We saved your request but could not send the confirmation email. "
        "Try again later or contact support."
    )
