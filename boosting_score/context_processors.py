"""Global template context."""

from boostingscore.plan_limits import plan_context_for_user
from vocabulary.models import UserProfile


def nav_section_for_path(path: str) -> str:
    """Return the primary nav section for the current URL path."""
    path = (path or "/").rstrip("/") + "/"
    if path == "/home/":
        return "home"
    prefixes = (
        ("/vocabulary/", "vocabulary"),
        ("/reading/", "reading"),
        ("/writing/", "writing"),
        ("/listening/", "listening"),
        ("/speaking/", "speaking"),
    )
    for prefix, section in prefixes:
        if path.startswith(prefix):
            return section
    return ""


def streak_context(request):
    """Expose streak for nav and base templates on every page."""
    ctx = {
        "streak": 0,
        "best_streak": 0,
        "nav_section": nav_section_for_path(getattr(request, "path", "")),
    }
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        ctx["streak"] = profile.streak or 0
        ctx["best_streak"] = profile.best_streak or 0
        ctx["speaking_ai_notice_needed"] = not bool(
            getattr(profile, "speaking_ai_notice_seen", False)
        )
        ctx["level_badge_text"] = profile.level_badge_text
        ctx["placement_completed"] = bool(profile.placement_completed)
        name = (request.user.first_name or request.user.username or "U").strip()
        ctx["avatar_initial"] = (name[:1] or "U").upper()
        ctx.update(plan_context_for_user(request.user))
    else:
        ctx["avatar_initial"] = "U"
    return ctx
