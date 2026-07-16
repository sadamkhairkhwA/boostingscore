"""In-app feedback widget — submit endpoint."""

from __future__ import annotations

import json
from datetime import timedelta

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


def _payload(request) -> dict:
    content_type = (request.META.get("CONTENT_TYPE") or "").split(";")[0].strip().lower()
    if content_type == "application/json":
        try:
            data = json.loads(request.body.decode("utf-8") or "{}")
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    return {
        "type": request.POST.get("type", ""),
        "message": request.POST.get("message", ""),
        "page_url": request.POST.get("page_url", ""),
        "user_agent": request.POST.get("user_agent", ""),
        "email": request.POST.get("email", ""),
    }


@require_POST
def feedback_submit(request):
    """Accept feedback; always return JSON (including when rate-limited)."""
    if not request.user.is_authenticated:
        return JsonResponse(
            {"ok": False, "error": "Please log in to send feedback."},
            status=401,
        )

    payload = _payload(request)

    message = str(payload.get("message") or "").strip()
    if not message:
        return JsonResponse(
            {"ok": False, "error": "Please write a short message."},
            status=400,
        )
    if len(message) > MAX_MESSAGE_LEN:
        message = message[:MAX_MESSAGE_LEN]

    feedback_type = (
        str(payload.get("type") or FeedbackSubmission.TYPE_SUGGESTION).strip().lower()
    )
    if feedback_type not in ALLOWED_TYPES:
        feedback_type = FeedbackSubmission.TYPE_SUGGESTION

    page_url = str(payload.get("page_url") or "").strip()[:500]
    user_agent = (request.META.get("HTTP_USER_AGENT") or "")[:1000]
    if not user_agent:
        user_agent = str(payload.get("user_agent") or "").strip()[:1000]

    email = (getattr(request.user, "email", None) or "").strip()
    if not email:
        email = str(payload.get("email") or "").strip()[:254]

    since = timezone.now() - timedelta(hours=1)
    try:
        recent = FeedbackSubmission.objects.filter(
            user=request.user, created_at__gte=since
        ).count()
    except Exception:
        return JsonResponse(
            {
                "ok": False,
                "error": "Feedback storage isn't ready yet. Please try again shortly.",
            },
            status=503,
        )

    if recent >= MAX_PER_HOUR:
        return _thanks()

    try:
        FeedbackSubmission.objects.create(
            user=request.user,
            email=email,
            feedback_type=feedback_type,
            message=message,
            page_url=page_url,
            user_agent=user_agent,
        )
    except Exception:
        return JsonResponse(
            {
                "ok": False,
                "error": "Couldn't save your feedback. Please try again shortly.",
            },
            status=500,
        )
    return _thanks()
