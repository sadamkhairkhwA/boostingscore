"""Daily streak updates for UserProfile."""

from django.utils import timezone

from .models import UserProfile


def bump_streak_for_user(user):
    """Increment streak on consecutive calendar days of activity; reset if a day was missed."""
    if not user or not user.is_authenticated:
        return
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    today = timezone.localdate()
    last = profile.last_activity_date
    if last is None:
        profile.streak = 1
    elif last == today:
        pass
    elif (today - last).days == 1:
        profile.streak = (profile.streak or 0) + 1
    else:
        profile.streak = 1

    profile.last_activity_date = today
    if (profile.streak or 0) > (profile.best_streak or 0):
        profile.best_streak = profile.streak
    profile.save(update_fields=["streak", "best_streak", "last_activity_date"])
