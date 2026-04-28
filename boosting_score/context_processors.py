"""Global template context."""

from vocabulary.models import UserProfile


def streak_context(request):
    """Expose streak for nav and base templates on every page."""
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        return {
            "streak": profile.streak or 0,
            "best_streak": profile.best_streak or 0,
        }
    return {"streak": 0, "best_streak": 0}
