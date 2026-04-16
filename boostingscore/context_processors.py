from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from boostingscore.models import UserProfile


def _activity_dates_for_user(user):
    from vocabulary.models import CustomCard
    from writing.models import Essay, WordBankEntry

    dates = set()
    for d in Essay.objects.filter(student=user).values_list("submitted_at", flat=True):
        dates.add(timezone.localdate(d))
    for d in WordBankEntry.objects.filter(user=user).values_list("created_at", flat=True):
        dates.add(timezone.localdate(d))
    for d in CustomCard.objects.filter(student=user).values_list("created_at", flat=True):
        dates.add(timezone.localdate(d))
    return dates


def study_streak(user) -> int:
    if not user.is_authenticated:
        return 0
    dates = _activity_dates_for_user(user)
    d = timezone.localdate()
    streak = 0
    while d in dates:
        streak += 1
        d -= timedelta(days=1)
    return streak


def words_learned_today(user) -> int:
    if not user.is_authenticated:
        return 0
    from vocabulary.models import CustomCard
    from writing.models import WordBankEntry

    today = timezone.localdate()
    c1 = CustomCard.objects.filter(student=user, created_at__date=today).count()
    c2 = WordBankEntry.objects.filter(user=user, created_at__date=today).count()
    return c1 + c2


_LEVEL_LABELS = {1: "Beginner", 2: "Standard", 3: "Advanced"}


def global_nav(request):
    nav_vocab_level = None
    nav_vocab_level_label = ""
    if request.user.is_authenticated:
        p = UserProfile.objects.filter(user=request.user).values("level").first()
        if p:
            nav_vocab_level = p["level"]
            nav_vocab_level_label = _LEVEL_LABELS.get(nav_vocab_level, "")
    return {
        "nav_streak": study_streak(request.user),
        "words_today_count": words_learned_today(request.user),
        "static_css_version": getattr(settings, "STATIC_CSS_VERSION", "1"),
        "nav_vocab_level": nav_vocab_level,
        "nav_vocab_level_label": nav_vocab_level_label,
    }
