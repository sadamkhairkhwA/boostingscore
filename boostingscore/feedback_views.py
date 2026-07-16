"""In-app feedback widget — JSON submit endpoint."""

from __future__ import annotations

import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from vocabulary.models import FeedbackSubmission

MAX_PER_HOUR = 5
MAX_MESSAGE_LEN = 4000
ALLOWED_TYPES = {
    FeedbackSubmission.TYPE_BUG,
    FeedbackSubmission.TYPE_SUGGESTION,
    FeedbackSubmission.TYPE_OTHER,
}


def _thanks() -> JsonResponse:
    return JsonResponse({"ok": True, "message": "Thanks — got it!"})


@login_required
@require_POST
def feedback_submit(request):
    """Accept feedback JSON; always return a friendly thanks (including when rate-limited)."""
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}

    message = str(payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"ok": False, "error": "Please write a short message."}, status=400)
    if len(message) > MAX_MESSAGE_LEN:
        message = message[:MAX_MESSAGE_LEN]

    feedback_type = str(payload.get("type") or FeedbackSubmission.TYPE_SUGGESTION).strip().lower()
    if feedback_type not in ALLOWED_TYPES:
        feedback_type = FeedbackSubmission.TYPE_SUGGESTION

    page_url = str(payload.get("page_url") or "").strip()[:500]
    user_agent = (request.META.get("HTTP_USER_AGENT") or "")[:1000]
    # Prefer client-sent UA only as fallback; server header is authoritative.
    if not user_agent:
        user_agent = str(payload.get("user_agent") or "").strip()[:1000]

    email = (getattr(request.user, "email", None) or "").strip()
    if not email:
        email = str(payload.get("email") or "").strip()[:254]

    since = timezone.now() - timedelta(hours=1)
    recent = FeedbackSubmission.objects.filter(
        user=request.user, created_at__gte=since
    ).count()
    if recent >= MAX_PER_HOUR:
        return _thanks()

    FeedbackSubmission.objects.create(
        user=request.user,
        email=email,
        feedback_type=feedback_type,
        message=message,
        page_url=page_url,
        user_agent=user_agent,
    )
    return _thanks()
