"""Maintenance mode: show a branded 503 page to everyone except admin/staff.

The flag is read from the database on every request, so toggling it in
Django admin takes effect immediately — no caching, no redeploy.
"""
from __future__ import annotations

import logging

from django.http import HttpResponse
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

# Prevent browsers / reverse proxies from serving a stale homepage after
# maintenance is toggled on (or a stale 503 after it is toggled off).
_NO_STORE = "no-store, no-cache, must-revalidate, max-age=0"


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin must always work so maintenance mode can be turned back off.
        # Match /admin and /admin/… (trailing slash optional).
        if request.path == "/admin" or request.path.startswith("/admin/"):
            return self.get_response(request)

        # Staff/superusers browse the site normally during maintenance.
        user = getattr(request, "user", None)
        if (
            user is not None
            and getattr(user, "is_authenticated", False)
            and getattr(user, "is_staff", False)
        ):
            return self.get_response(request)

        try:
            from vocabulary.models import SiteSettings

            # Always read pk=1 fresh from the DB (no cache layer).
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
            response = self.get_response(request)
            # Stop browsers holding a cached 200 of the homepage across a
            # later maintenance toggle (especially on the landing page).
            if request.path in ("/", "") or request.path.startswith("/home"):
                response["Cache-Control"] = _NO_STORE
                response["Pragma"] = "no-cache"
            return response

        logger.info(
            "maintenance mode active — serving 503 for %s %s",
            request.method,
            request.path,
        )
        html = render_to_string(
            "maintenance.html",
            {"message": row["maintenance_message"] or ""},
            request=request,
        )
        response = HttpResponse(html, status=503)
        response["Retry-After"] = "600"
        response["Cache-Control"] = _NO_STORE
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        response["X-BoostingScore-Maintenance"] = "1"
        return response
