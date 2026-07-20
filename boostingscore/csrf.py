"""Clearer CSRF failure page + diagnostics for production 403s."""
from __future__ import annotations

import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    """Log why CSRF failed and show a recoverable page instead of Django's blank 403."""
    logger.warning(
        "CSRF failure: reason=%r path=%s method=%s origin=%r referer=%r "
        "host=%s secure=%s has_csrf_cookie=%s",
        reason,
        request.path,
        request.method,
        request.META.get("HTTP_ORIGIN"),
        request.META.get("HTTP_REFERER"),
        request.get_host(),
        request.is_secure(),
        "csrftoken" in request.COOKIES or "csrftoken_v2" in request.COOKIES,
    )
    return render(
        request,
        "csrf_failure.html",
        {
            "reason": reason,
            "next_url": request.path,
        },
        status=403,
    )
