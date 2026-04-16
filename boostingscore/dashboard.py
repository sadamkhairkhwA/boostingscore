"""Context builders for the logged-in home dashboard."""

from __future__ import annotations

from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models import Count, Q

from reading.models import IELTSTestResult
from vocabulary.models import CustomCard
from writing.models import Essay, WordBankEntry


def greeting_name(user: User) -> str:
    name = (user.first_name or "").strip()
    return name or user.username


def greeting_time_label() -> str:
    h = timezone.localtime().hour
    if h < 12:
        return "Good morning"
    if h < 17:
        return "Good afternoon"
    return "Good evening"


def home_dashboard_context(user: User, request=None) -> dict:
    now = timezone.now()
    latest = Essay.objects.filter(student=user).order_by("-submitted_at").first()
    band = latest.band_score if latest and latest.band_score is not None else None

    vocab_qs = CustomCard.objects.filter(student=user)
    vocab_total = vocab_qs.count()
    vocab_due = vocab_qs.filter(
        Q(next_review_at__isnull=True) | Q(next_review_at__lte=now),
        is_mastered=False,
    ).count()
    vocab_mastered = vocab_qs.filter(is_mastered=True).count()
    topic_row = vocab_qs.values("topic").annotate(c=Count("id")).order_by("-c").first()
    vocab_topic_label = (
        dict(CustomCard.TOPIC_CHOICES).get(topic_row["topic"], "Mixed topics")
        if topic_row
        else "Your topics"
    )

    word_bank_count = WordBankEntry.objects.filter(user=user).count()
    essay_count = Essay.objects.filter(student=user).count()

    words_learned = vocab_total + word_bank_count

    passages_done = 0
    if request is not None:
        passages_done = int(request.session.get("reading_quiz_completions", 0))

    # Reading app now tracks IELTS attempts instead of static passage rows.
    reading_passages_total = 10
    reading_done_db = IELTSTestResult.objects.filter(student=user).count()
    if reading_done_db > passages_done:
        passages_done = reading_done_db
    reading_pct = min(100, int(100 * passages_done / reading_passages_total))
    vocab_pct = min(100, int(100 * vocab_mastered / max(vocab_total, 1))) if vocab_total else 0
    writing_pct = min(100, essay_count * 20)
    word_bank_pct = min(100, word_bank_count * 12)

    from boostingscore.context_processors import study_streak

    streak = study_streak(user)

    study_plan = [
        {
            "task": "Review 10 vocabulary cards in your weakest topic",
            "mins": 12,
            "tone": "green",
        },
        {
            "task": "Complete one reading passage with comprehension check",
            "mins": 20,
            "tone": "blue",
        },
        {
            "task": "Write 250+ words for Task 2 and review AI feedback",
            "mins": 40,
            "tone": "purple",
        },
        {
            "task": "Add 3 new words to your word bank from feedback",
            "mins": 8,
            "tone": "orange",
        },
    ]

    def _activity_kind(text: str) -> str:
        low = text.lower()
        if "word bank" in low:
            return "word_bank"
        if "writing" in low or "task" in low or "essay" in low:
            return "writing"
        if "vocabulary" in low:
            return "vocabulary"
        if "account" in low or "welcome" in low:
            return "account"
        return "vocabulary"

    activities: list[tuple[str, timezone.datetime]] = []
    for e in Essay.objects.filter(student=user).order_by("-submitted_at")[:5]:
        b = e.band_score if e.band_score is not None else "—"
        activities.append((f"Writing · Task 2 submitted · Band {b}", e.submitted_at))
    if vocab_total:
        latest_vocab = vocab_qs.order_by("-created_at").first()
        vc_at = latest_vocab.created_at if latest_vocab else now
        activities.append(
            (
                f"Vocabulary · Learned {vocab_total} new word{'s' if vocab_total != 1 else ''} · {vocab_topic_label}",
                vc_at,
            )
        )
    for w in WordBankEntry.objects.filter(user=user).order_by("-created_at")[:5]:
        activities.append(("Word bank · Added phrase from learning", w.created_at))
    activities.append(("Account created • Welcome to Boosting Score", user.date_joined))
    activities.sort(key=lambda x: x[1], reverse=True)
    recent_activity = [
        {"text": t, "when": d, "kind": _activity_kind(t)} for t, d in activities[:5]
    ]

    words_target = 200
    words_target_pct = min(100, int(100 * words_learned / max(words_target, 1)))

    if band is None:
        dash_band_hint = "Write an essay to get your first score."
    else:
        dash_band_hint = "Based on your latest submitted essay."
    dash_words_hint = f"Target: {words_target} IELTS words"
    if passages_done == 0:
        dash_passages_hint = "Start your first reading passage."
    else:
        dash_passages_hint = f"{passages_done} passage{'s' if passages_done != 1 else ''} completed — keep going."
    if streak == 0:
        dash_streak_hint = "Study today to start your streak."
    else:
        dash_streak_hint = "Keep logging in daily to grow your streak."

    if vocab_due:
        dash_status_line = (
            f"You have {vocab_due} vocabulary word{'s' if vocab_due != 1 else ''} "
            "due for review and a study plan waiting for you."
        )
    else:
        dash_status_line = (
            "You're caught up on reviews — open your study plan or jump into reading or writing."
        )

    return {
        "dash_greeting": greeting_time_label(),
        "dash_name": greeting_name(user),
        "dash_band": band,
        "dash_words": words_learned,
        "dash_passages": passages_done,
        "dash_streak": streak,
        "study_plan": study_plan,
        "recent_activity": recent_activity,
        "skill_vocab_level": 4,
        "skill_reading_level": 3,
        "skill_writing_level": 2,
        "skill_listening_level": 1,
        "skill_listening_bar": 8,
        "skill_vocab_bar": 82,
        "skill_reading_bar": 42,
        "skill_writing_bar": 28,
        "words_target": words_target,
        "words_target_pct": words_target_pct,
        "dash_band_hint": dash_band_hint,
        "dash_words_hint": dash_words_hint,
        "dash_passages_hint": dash_passages_hint,
        "dash_streak_hint": dash_streak_hint,
        "dash_vocab_due": vocab_due,
        "dash_vocab_total": vocab_total,
        "dash_vocab_mastered": vocab_mastered,
        "dash_vocab_topic": vocab_topic_label,
        "dash_vocab_pct": vocab_pct,
        "dash_word_bank_count": word_bank_count,
        "dash_essay_count": essay_count,
        "dash_reading_ready": reading_passages_total,
        "dash_reading_pct": reading_pct,
        "dash_writing_pct": writing_pct,
        "dash_word_bank_pct": word_bank_pct,
        "dash_status_line": dash_status_line,
    }


def flat_home_page_context(user: User, request=None) -> dict:
    """Flat template variables for ``templates/home.html`` (bands, stats, activity)."""
    band_score = None
    words_learned = 0
    words_pct = 0
    passages_done = 0
    streak = 0
    best_streak = 0
    essays_count = 0
    wordbank_count = 0
    recent_activity: list[dict] = []

    try:
        dash = home_dashboard_context(user, request)
    except Exception:
        dash = {}

    try:
        band_score = dash.get("dash_band")
    except Exception:
        band_score = None

    try:
        words_learned = int(dash.get("dash_words") or 0)
    except Exception:
        words_learned = 0

    try:
        words_target = int(dash.get("words_target") or 200)
        words_pct = min(100, int(100 * words_learned / max(words_target, 1)))
    except Exception:
        words_pct = 0

    try:
        passages_done = int(dash.get("dash_passages") or 0)
    except Exception:
        passages_done = 0

    try:
        streak = int(dash.get("dash_streak") or 0)
    except Exception:
        streak = 0

    try:
        p = getattr(user, "profile", None)
        if p is not None:
            best_streak = int(getattr(p, "best_streak", 0) or 0)
    except Exception:
        best_streak = 0

    try:
        essays_count = int(dash.get("dash_essay_count") or 0)
    except Exception:
        essays_count = 0

    try:
        wordbank_count = int(dash.get("dash_word_bank_count") or 0)
    except Exception:
        wordbank_count = 0

    try:
        for row in dash.get("recent_activity") or []:
            recent_activity.append(
                {
                    "text": row.get("text", ""),
                    "timestamp": row.get("when"),
                }
            )
    except Exception:
        recent_activity = []

    return {
        "band_score": band_score,
        "words_learned": words_learned,
        "words_pct": words_pct,
        "passages_done": passages_done,
        "streak": streak,
        "best_streak": best_streak,
        "essays_count": essays_count,
        "wordbank_count": wordbank_count,
        "recent_activity": recent_activity,
    }
