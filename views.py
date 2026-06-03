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

    # ---------------- Vocabulary stats ----------------
    studied_topic_counts: dict[str, int] = {}
    studied_word_ids: list[int] = []
    type_it_done = False
    try:
        from vocabulary.models import VocabularyProgress, Word, TypeItAttempt

        now = timezone.now()
        all_prog = VocabularyProgress.objects.filter(student=user)
        words_learned = all_prog.count()
        mastered_count = all_prog.filter(mastery_level=5).count()
        mastered_pct = round(mastered_count / words_learned * 100) if words_learned else 0
        due_count = all_prog.filter(next_review__lte=now).count()
        week_ago = now - timezone.timedelta(days=7)
        words_this_week = all_prog.filter(last_reviewed__gte=week_ago).count()

        studied_word_ids = list(
            all_prog.filter(word__isnull=False).values_list("word_id", flat=True)
        )
        if studied_word_ids:
            studied_topic_counts = dict(
                Word.objects.filter(id__in=studied_word_ids)
                .values_list("topic")
                .annotate(c=models_count())
            )

        type_it_done = TypeItAttempt.objects.filter(student=user).exists()
    except Exception:
        pass

    try:
        from reading.models import ReadingAttempt

        reading_done = ReadingAttempt.objects.filter(student=user, completed=True).count()
        reading_pct = min(reading_done * 2, 100)
    except Exception:
        pass

    # Combined "tests taken" across academic + IELTS test runs
    tests_taken = 0
    try:
        from reading.models import ReadingTestResult, IELTSTestResult, ReadingAttempt as _RA

        tests_taken = (
            ReadingTestResult.objects.filter(user=user).count()
            + IELTSTestResult.objects.filter(student=user).count()
            + _RA.objects.filter(student=user, completed=True).count()
        )
    except Exception:
        pass
    tests_pct = min(tests_taken * 10, 100)

    # ---------------- Writing stats ----------------
    best_band_score = None
    essays_done = 0
    try:
        from writing.models import Essay, WritingTask1Attempt, WritingTask2Attempt

        legacy_essays = Essay.objects.filter(student=user)
        t1 = WritingTask1Attempt.objects.filter(user=user)
        t2 = WritingTask2Attempt.objects.filter(user=user)
        essays_done = legacy_essays.count() + t1.count() + t2.count()

        bands = []
        for qs, field in (
            (legacy_essays, "band_score"),
            (t1, "band_score"),
            (t2, "band_score"),
        ):
            top = qs.exclude(**{f"{field}__isnull": True}).order_by(f"-{field}").first()
            if top is not None and getattr(top, field, None) is not None:
                bands.append(float(getattr(top, field)))
        if bands:
            best_band_score = round(max(bands), 1)
    except Exception:
        pass

    # ---------------- Lessons / skills progress ----------------
    lessons_done = 0
    skills_done = 0
    try:
        from writing.models import LessonProgress, SkillProgress

        lessons_done = LessonProgress.objects.filter(user=user).count()
        skills_done = SkillProgress.objects.filter(user=user).count()
    except Exception:
        pass

    # ---------------- "Get started" 4-step checklist ----------------
    steps = [
        {
            "n": 1,
            "title": "Study your first vocabulary word",
            "sub": "Go to Vocabulary and learn one word",
            "url_name": "vocabulary:home",
            "done": words_learned > 0,
        },
        {
            "n": 2,
            "title": "Complete a Type-it session",
            "sub": "Write a definition and sentence from memory",
            "url_name": "vocabulary:type_it_deck",
            "done": type_it_done,
        },
        {
            "n": 3,
            "title": "Write your first Task 1 essay",
            "sub": "Get AI band score with inline feedback",
            "url_name": "writing:task1",
            "done": (essays_done > 0),
        },
        {
            "n": 4,
            "title": "Read your first writing lesson",
            "sub": "Learn the 4-paragraph structure for Task 1",
            "url_name": "writing:lessons_hub",
            "done": lessons_done > 0,
        },
    ]
    steps_done = sum(1 for s in steps if s["done"])
    show_get_started = steps_done < 4

    # ---------------- Today's plan ----------------
    today_tasks = [
        {
            "title": "10 vocabulary words",
            "sub": "Health topic · Beginner",
            "url_name": "vocabulary:home",
            "icon": "book",
            "done": words_this_week >= 10,
        },
        {
            "title": "1 Type-it session",
            "sub": "Write from memory",
            "url_name": "vocabulary:type_it_deck",
            "icon": "pencil",
            "done": type_it_done,
        },
        {
            "title": "Read Task 1 lesson",
            "sub": "The 4-paragraph structure",
            "url_name": "writing:lessons_hub",
            "icon": "school",
            "done": lessons_done > 0,
        },
    ]
    # Mark first incomplete task as primary
    next_primary_set = False
    for t in today_tasks:
        t["primary"] = not t["done"] and not next_primary_set
        if t["primary"]:
            next_primary_set = True

    # ---------------- Vocabulary topics row ----------------
    TOPIC_META = [
        ("health",      "Health",      "heartbeat", "blue"),
        ("environment", "Environment", "leaf",      "green"),
        ("technology",  "Technology",  "laptop",    "purple"),
        ("society",     "Society",     "community", "amber"),
    ]
    total_words_by_topic: dict[str, int] = {}
    try:
        from vocabulary.models import Word

        total_words_by_topic = dict(
            Word.objects.values_list("topic").annotate(c=models_count())
        )
    except Exception:
        pass

    vocab_topics = []
    for slug, name, icon, colour in TOPIC_META:
        total = total_words_by_topic.get(slug, 0)
        # Fallback nice-looking baselines so progress bars don't all read 0% during initial seeding
        if not total:
            total = {"health": 180, "environment": 165, "technology": 190, "society": 175}.get(slug, 150)
        studied = studied_topic_counts.get(slug, 0)
        pct = round(studied / total * 100) if total else 0
        vocab_topics.append({
            "slug": slug, "name": name, "icon": icon, "colour": colour,
            "studied": studied, "total": total, "pct": min(pct, 100),
        })

    # ---------------- Recent activity (last 5, merged from all sources) ----------------
    recent: list[dict] = []
    try:
        from vocabulary.models import TypeItAttempt
        for a in TypeItAttempt.objects.filter(student=user).order_by("-created_at")[:5]:
            label_word = (a.word.word if a.word_id else (a.custom_word.word if a.custom_word_id else "—"))
            recent.append({
                "icon": "pencil",
                "title": f"Type-it · {label_word}",
                "sub": f"Score {a.total_score} / 10",
                "when": a.created_at,
                "url_name": "vocabulary:type_it_deck",
            })
    except Exception:
        pass
    try:
        from writing.models import WritingTask1Attempt, WritingTask2Attempt
        for a in WritingTask1Attempt.objects.filter(user=user).order_by("-completed_at")[:5]:
            recent.append({
                "icon": "file",
                "title": f"Task 1 · {a.question_type.replace('-', ' ').title()}",
                "sub": f"Band {a.band_score:.1f} · {a.word_count} words",
                "when": a.completed_at,
                "url_name": "writing:task1",
            })
        for a in WritingTask2Attempt.objects.filter(user=user).order_by("-completed_at")[:5]:
            recent.append({
                "icon": "file",
                "title": f"Task 2 · {a.essay_type.replace('-', ' ').title()}",
                "sub": f"Band {a.band_score:.1f} · {a.word_count} words",
                "when": a.completed_at,
                "url_name": "writing:task2",
            })
    except Exception:
        pass
    recent.sort(key=lambda r: r["when"], reverse=True)
    recent = recent[:5]

    # ---------------- Writing % (rough, for the progress card) ----------------
    writing_pct = min((essays_done or 0) * 10, 100)
    vocab_pct = mastered_pct  # already computed
    lessons_total = 18

    sessions_done_total = words_learned + (1 if type_it_done else 0) + essays_done + lessons_done
    show_new_tip = sessions_done_total < 5

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

            # New dashboard context
            "steps": steps,
            "steps_done": steps_done,
            "show_get_started": show_get_started,
            "show_new_tip": show_new_tip,
            "today_tasks": today_tasks,
            "vocab_topics": vocab_topics,
            "recent": recent,
            "best_band_score": best_band_score,
            "lessons_done": lessons_done,
            "lessons_total": lessons_total,
            "vocab_pct": vocab_pct,
            "writing_pct": writing_pct,
            "tests_taken": tests_taken,
            "tests_pct": tests_pct,
        },
    )


def models_count():
    """Tiny shim so we can do .annotate(c=models_count()) without polluting imports."""
    from django.db.models import Count
    return Count("id")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # No AUTH_PASSWORD_VALIDATORS are configured, so enforce our own
        # minimums here (mirrors the inline rules shown on the form):
        # username >= 3 characters, password >= 8 characters.
        if form.is_valid():
            username = form.cleaned_data.get("username", "")
            password = form.cleaned_data.get("password1", "")
            if len(username) < 3:
                form.add_error("username", "Username must be at least 3 characters.")
            if len(password) < 8:
                form.add_error("password2", "Password must be at least 8 characters.")
            if not form.errors:
                user = form.save()
                login(request, user)
                return redirect("welcome")
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
