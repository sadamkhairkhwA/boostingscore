"""Maintenance mode: show a branded 503 page to everyone except admin/staff.

The flag is read from the database on every request, so toggling it in
Django admin takes effect immediately — no caching, no redeploy.
"""
from __future__ import annotations

import logging

from django.http import HttpResponse
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin must always work so maintenance mode can be turned back off.
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Staff/superusers browse the site normally during maintenance.
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated and user.is_staff:
            return self.get_response(request)

        try:
            from vocabulary.models import SiteSettings

            row = (
                SiteSettings.objects.filter(pk=1)
                .values("maintenance_mode", "maintenance_message")
                .first()
            )
        except Exception as exc:
            # Fail open (e.g. before the migration has run) — never take the
            # site down because the settings row is unreadable.
            logger.warning("maintenance check failed: %s", exc)
            row = None

        if not row or not row["maintenance_mode"]:
            return self.get_response(request)

        html = render_to_string(
            "maintenance.html",
            {"message": row["maintenance_message"]},
            request=request,
        )
        response = HttpResponse(html, status=503)
        response["Retry-After"] = "600"
        return response
