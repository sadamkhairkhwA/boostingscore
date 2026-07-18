"""HTTPS email backends for hosts that block outbound SMTP (e.g. Railway Hobby).

Resend's REST API runs over HTTPS (port 443), which Railway does not block,
unlike SMTP ports 25/465/587 on Free/Trial/Hobby plans.
"""
from __future__ import annotations

import logging
from email.utils import parseaddr

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

RESEND_SEND_URL = "https://api.resend.com/emails"


class ResendAPIEmailBackend(BaseEmailBackend):
    """Send mail via Resend's REST API (HTTPS :443) instead of SMTP :587.

    Used as a drop-in Django email backend, so everything that goes through
    ``django.core.mail`` (signup verification, email change, password reset)
    is delivered over HTTPS automatically.
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        api_key = (getattr(settings, "RESEND_API_KEY", "") or "").strip()
        if not api_key:
            if self.fail_silently:
                logger.warning("RESEND_API_KEY is not set; dropping %d email(s).", len(email_messages))
                return 0
            raise RuntimeError("RESEND_API_KEY is not set; cannot send via ResendAPIEmailBackend.")

        timeout = float(getattr(settings, "EMAIL_TIMEOUT", 8) or 8)
        sent = 0
        for message in email_messages:
            try:
                if self._send_one(message, api_key, timeout):
                    sent += 1
            except Exception as exc:
                logger.warning("Resend API send failed: %s", exc)
                if not self.fail_silently:
                    raise
        return sent

    def _send_one(self, message, api_key: str, timeout: float) -> bool:
        recipients = [addr for addr in message.to if addr]
        if not recipients:
            return False

        payload: dict = {
            "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
            "to": recipients,
            "subject": message.subject or "",
        }

        body = message.body or ""
        if message.content_subtype == "html":
            payload["html"] = body
        else:
            payload["text"] = body
        # Include the HTML alternative if the message carries one
        # (e.g. Django's password reset with html_email_template_name).
        for content, mimetype in getattr(message, "alternatives", []) or []:
            if mimetype == "text/html":
                payload["html"] = content
                break

        if message.cc:
            payload["cc"] = list(message.cc)
        if message.bcc:
            payload["bcc"] = list(message.bcc)
        if message.reply_to:
            _, reply_email = parseaddr(message.reply_to[0])
            if reply_email:
                payload["reply_to"] = reply_email

        response = requests.post(
            RESEND_SEND_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"Resend API HTTP {response.status_code}: {response.text[:500]}"
            )
        return True
