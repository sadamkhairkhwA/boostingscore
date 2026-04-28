from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


def get_streak(user):
    return getattr(getattr(user, "profile", None), "streak", 0) or 0


@login_required
def home_view(request):
    user = request.user
    hour = timezone.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    words_learned = mastered_count = mastered_pct = due_count = words_this_week = 0
    reading_done = reading_pct = essays_done = 0
    streak = get_streak(user)
    best_streak = getattr(getattr(user, "profile", None), "best_streak", 0) or 0

    try:
        from vocabulary.models import VocabularyProgress

        now = timezone.now()
        all_prog = VocabularyProgress.objects.filter(student=user)
        words_learned = all_prog.count()
        mastered_count = all_prog.filter(mastery_level=5).count()
        mastered_pct = round(mastered_count / words_learned * 100) if words_learned else 0
        due_count = all_prog.filter(next_review__lte=now).count()
        week_ago = now - timezone.timedelta(days=7)
        words_this_week = all_prog.filter(last_reviewed__gte=week_ago).count()
    except Exception:
        pass

    try:
        from reading.models import ReadingAttempt

        reading_done = ReadingAttempt.objects.filter(student=user, completed=True).count()
        reading_pct = min(reading_done * 2, 100)
    except Exception:
        pass

    try:
        from writing.models import Essay

        essays_done = Essay.objects.filter(student=user).count()
    except Exception:
        pass

    return render(
        request,
        "home.html",
        {
            "greeting": greeting,
            "words_learned": words_learned,
            "words_this_week": words_this_week,
            "mastered_count": mastered_count,
            "mastered_pct": mastered_pct,
            "due_count": due_count,
            "streak": streak,
            "best_streak": best_streak,
            "reading_done": reading_done,
            "reading_pct": reading_pct,
            "essays_done": essays_done,
        },
    )


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile_settings(request):
    from vocabulary.models import UserProfile
    from reading.models import ReadingTestResult

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    level_label = {1: "Beginner", 2: "Standard", 3: "Advanced"}.get(profile.level, "Beginner")
    reading_history = (
        ReadingTestResult.objects.filter(user=request.user)
        .select_related("test")
        .order_by("-completed_at")[:25]
    )
    return render(
        request,
        "profile_settings.html",
        {
            "profile": profile,
            "level_label": level_label,
            "reading_history": reading_history,
        },
    )
