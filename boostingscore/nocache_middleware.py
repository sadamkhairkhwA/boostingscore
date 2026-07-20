"""Prevent browsers from caching auth/admin HTML with stale CSRF tokens."""
from __future__ import annotations


class NoCacheAuthPagesMiddleware:
    """Auth and admin forms must never be served from bfcache/disk cache.

    After SECRET_KEY or cookie-name rotations, a cached login page posts an
    old csrfmiddlewaretoken and Django returns 403. no-store fixes that.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path or ""
        if path.startswith("/admin") or path.startswith("/accounts"):
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response
