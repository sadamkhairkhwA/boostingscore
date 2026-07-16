"""Inject the floating feedback widget on every authenticated HTML page."""

from __future__ import annotations

from django.template.loader import render_to_string


class FeedbackWidgetMiddleware:
    """Append the feedback FAB before </body> when the user is logged in.

    Skips responses that already include the widget (template includes) so we
    never double-inject. Covers standalone shells that don't extend base.html.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return response
        if getattr(response, "streaming", False):
            return response
        if response.status_code != 200:
            return response

        content_type = (response.get("Content-Type") or "").split(";")[0].strip().lower()
        if content_type and content_type != "text/html":
            return response

        try:
            content = response.content
        except Exception:
            return response

        if b'id="bs-feedback"' in content or b"id='bs-feedback'" in content:
            return response

        lower = content.lower()
        marker = b"</body>"
        idx = lower.rfind(marker)
        if idx == -1:
            return response

        try:
            from django.middleware.csrf import get_token

            get_token(request)  # ensure CSR cookie is set on this response
            widget = render_to_string(
                "includes/feedback_widget.html",
                request=request,
            ).encode(response.charset or "utf-8")
        except Exception:
            return response

        if not widget.strip():
            return response

        response.content = content[:idx] + widget + content[idx:]
        if response.has_header("Content-Length"):
            response["Content-Length"] = str(len(response.content))
        return response
