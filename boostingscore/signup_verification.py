"""Signup email verification via a 6-digit code.

New accounts are created inactive; the user types the emailed code on the
check-email page to activate. No tokenized links — code-based only.

IMPORTANT: email delivery must never prevent or roll back account creation.
Callers must save the User first; this module only sends mail and never raises.
"""
from __future__ import annotations

import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

CODE_TTL_MINUTES = 15
MAX_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 60

FALLBACK_MSG = (
    "Account created — if you don't receive an email shortly, "
    "use Resend below or contact support."
)


def _using_console_email() -> bool:
    backend = (getattr(settings, "EMAIL_BACKEND", "") or "").lower()
    return "console" in backend or "locmem" in backend or "dummy" in backend


def _show_dev_code() -> bool:
    """Only reveal the code in the UI when no real email leaves the machine."""
    return _using_console_email() or settings.DEBUG


def issue_signup_code(user) -> str:
    """Create (or replace) the user's 6-digit code with a fresh 15-min expiry."""
    from vocabulary.models import SignupCode

    code = f"{secrets.randbelow(1_000_000):06d}"
    SignupCode.objects.update_or_create(
        user=user,
        defaults={
            "code": code,
            "created_at": timezone.now(),
            "expires_at": timezone.now() + timedelta(minutes=CODE_TTL_MINUTES),
            "attempts": 0,
        },
    )
    return code


def resend_allowed(user) -> bool:
    """Basic rate limit: one code per RESEND_COOLDOWN_SECONDS."""
    from vocabulary.models import SignupCode

    row = SignupCode.objects.filter(user=user).first()
    if row is None:
        return True
    return (timezone.now() - row.created_at).total_seconds() >= RESEND_COOLDOWN_SECONDS


def verify_signup_code(user, submitted: str) -> tuple[bool, str]:
    """Check a submitted code. Returns (ok, error_message)."""
    from vocabulary.models import SignupCode

    submitted = (submitted or "").strip()
    if not submitted.isdigit() or len(submitted) != 6:
        return False, "Enter the 6-digit code from the email."

    row = SignupCode.objects.filter(user=user).first()
    if row is None:
        return False, "No code found — use Resend to get a new one."
    if timezone.now() > row.expires_at:
        return False, "This code has expired. Use Resend to get a new one."
    if row.attempts >= MAX_ATTEMPTS:
        return False, "Too many attempts. Use Resend to get a new code."

    if not secrets.compare_digest(row.code, submitted):
        row.attempts += 1
        row.save(update_fields=["attempts"])
        return False, "That code isn't right — check the email and try again."

    row.delete()
    return True, ""


def _email_bodies(code: str) -> tuple[str, str]:
    """Plain-text and inline-CSS HTML bodies for the verification email."""
    text = (
        f"Confirm your email\n\n"
        f"Enter this code to activate your account:\n\n"
        f"{code}\n\n"
        f"This code expires in {CODE_TTL_MINUTES} minutes.\n\n"
        f"If you didn't request this, you can ignore this email.\n"
        f"BoostingScore · boostingscore.com\n"
    )
    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f6f7f4;">
  <div style="max-width:440px;margin:0 auto;padding:32px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:32px 28px;">
      <p style="margin:0 0 24px;font-size:20px;font-weight:800;color:#111827;">
        Boosting<span style="color:#3B6D11;">Score</span>
      </p>
      <h1 style="margin:0 0 10px;font-size:18px;font-weight:700;color:#111827;">
        Confirm your email
      </h1>
      <p style="margin:0 0 20px;font-size:14px;line-height:1.5;color:#374151;">
        Enter this code to activate your account:
      </p>
      <div style="background:#EAF3DE;border-radius:10px;padding:18px 12px;text-align:center;margin:0 0 16px;">
        <span style="font-size:32px;font-weight:800;letter-spacing:8px;color:#27500A;">{code}</span>
      </div>
      <p style="margin:0 0 24px;font-size:13px;color:#374151;">
        This code expires in {CODE_TTL_MINUTES} minutes.
      </p>
      <p style="margin:0;font-size:12px;line-height:1.5;color:#9ca3af;">
        If you didn't request this, you can ignore this email.<br>
        BoostingScore · boostingscore.com
      </p>
    </div>
  </div>
</body>
</html>
"""
    return text, html


def _deliver_code_email(email: str, code: str) -> bool:
    """Attempt delivery. Returns True on success. Never raises."""
    try:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@boostingscore.com")
        text, html = _email_bodies(code)
        message = EmailMultiAlternatives(
            subject="Confirm your email — BoostingScore",
            body=text,
            from_email=from_email,
            to=[email],
        )
        message.attach_alternative(html, "text/html")
        return bool(message.send(fail_silently=False))
    except Exception as exc:
        logger.warning("signup verification send failed: %s", exc)
        return False


def send_signup_verification(request, user) -> tuple[bool, str, str]:
    """Issue a fresh code and email it to an already-saved (inactive) account.

    Always returns ``(True, message_for_user, dev_code_or_empty)`` so the
    signup view can show the check-email page. Failures are logged only.
    ``dev_code_or_empty`` is only populated in local/dev (console backend or
    DEBUG) so the page can display the code without a real inbox — never in
    production.

    In production, delivery is scheduled with ``transaction.on_commit`` so it
    cannot run (or hang) inside the same DB transaction as ``user.save()``.
    """
    email = (user.email or "").lower().strip()
    try:
        code = issue_signup_code(user)
    except Exception as exc:
        logger.warning("signup code issue failed for user_id=%s: %s", user.id, exc)
        return True, FALLBACK_MSG, ""

    if _show_dev_code():
        # Local/dev: send now so the console backend prints the email too.
        _deliver_code_email(email, code)
        return (
            True,
            "Local/dev mode: no real email is sent. Use the code shown below.",
            code,
        )

    def _send_after_commit():
        if not _deliver_code_email(email, code):
            logger.warning(
                "signup verification email not delivered for user_id=%s email=%s",
                user.id,
                email,
            )

    try:
        transaction.on_commit(_send_after_commit)
    except Exception as exc:
        logger.warning("signup on_commit schedule failed: %s", exc)
        _deliver_code_email(email, code)

    return (
        True,
        f"We sent a 6-digit code to {email}. Enter it below to activate your account.",
        "",
    )
