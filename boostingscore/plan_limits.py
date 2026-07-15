"""Free-plan limits and daily AI check quotas."""
from __future__ import annotations

from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import transaction
from django.db.models import F

IST = ZoneInfo("Europe/Istanbul")

PLAN_FREE = "free"
FREE_DAILY_AI_LIMIT = 10
FREE_PRACTICE_TEST_MAX = 1
FREE_ACADEMIC_READING_MAX = 1

PRACTICE_TEST_LOCK_MSG = "Free plan includes 1 practice test"
ACADEMIC_READING_LOCK_MSG = "Free plan includes 1 academic reading test"
AI_LIMIT_MSG = "Daily limit reached — resets tomorrow."
VOCAB_PREMIUM_LOCK_MSG = "Included in premium"
WRITING_TASK_USED_MSG = "Free attempt used"
WRITING_FREE_ATTEMPT_NOTE = "Free plan: 1 attempt"
FREE_WRITING_TASK_ATTEMPTS = 1

FEATURE_PRACTICE_TEST = "practice_test"
FEATURE_ACADEMIC_READING = "academic_reading"
FEATURE_WRITING_TASK1 = "writing_task1"
FEATURE_WRITING_TASK2 = "writing_task2"
FEATURE_WRITING_LESSONS = "writing_lessons"
FEATURE_WRITING_GRAMMAR = "writing_grammar"
FEATURE_WRITING_PARAPHRASE = "writing_paraphrase"
FEATURE_VOCAB_FLASHCARDS = "vocab_flashcards"
FEATURE_VOCAB_QUIZ = "vocab_quiz"
FEATURE_VOCAB_TYPE_IT = "vocab_type_it"
FEATURE_VOCAB_WORD_LIST = "vocab_word_list"
FEATURE_VOCAB_FAVORED = "vocab_favored"
FEATURE_VOCAB_GUIDE = "vocab_guide"
FEATURE_SPEAKING_QUESTIONS = "speaking_questions"
FEATURE_SPEAKING_PRONUNCIATION = "speaking_pronunciation"
FEATURE_SPEAKING_PHRASES = "speaking_phrases"
FEATURE_SPEAKING_TIPS = "speaking_tips"
FEATURE_SPEAKING_RECORD = "speaking_record"
FEATURE_READING_QUESTION_TYPES = "reading_question_types"
FEATURE_READING_STRATEGIES = "reading_strategies"
FEATURE_LISTENING_MULTIPLE_CHOICE = "listening_multiple_choice"
FEATURE_LISTENING_GAP_FILL = "listening_gap_fill"
FEATURE_LISTENING_SENTENCE = "listening_sentence"
FEATURE_LISTENING_MATCHING = "listening_matching"
FEATURE_LISTENING_MAP = "listening_map"
FEATURE_LISTENING_SHORT_ANSWER = "listening_short_answer"
FEATURE_LISTENING_SECTION4 = "listening_section4_notes"
FEATURE_LISTENING_DETAIL_DRILLS = "listening_detail_drills"

VOCAB_PREMIUM_FEATURES = frozenset(
    {
        FEATURE_VOCAB_QUIZ,
        FEATURE_VOCAB_TYPE_IT,
        FEATURE_VOCAB_WORD_LIST,
        FEATURE_VOCAB_FAVORED,
        FEATURE_VOCAB_GUIDE,
    }
)

VOCAB_FEATURE_LABELS = {
    FEATURE_VOCAB_QUIZ: "Quick quiz",
    FEATURE_VOCAB_TYPE_IT: "Type it",
    FEATURE_VOCAB_WORD_LIST: "Word list",
    FEATURE_VOCAB_FAVORED: "Favored words",
    FEATURE_VOCAB_GUIDE: "IELTS vocabulary guide",
}

WRITING_PREMIUM_FEATURES = frozenset(
    {
        FEATURE_WRITING_LESSONS,
        FEATURE_WRITING_GRAMMAR,
        FEATURE_WRITING_PARAPHRASE,
    }
)

WRITING_FEATURE_LABELS = {
    FEATURE_WRITING_LESSONS: "Writing lessons",
    FEATURE_WRITING_GRAMMAR: "Writing grammar",
    FEATURE_WRITING_PARAPHRASE: "Paraphrase practice",
}

SPEAKING_PREMIUM_FEATURES = frozenset(
    {
        FEATURE_SPEAKING_QUESTIONS,
        FEATURE_SPEAKING_PRONUNCIATION,
        FEATURE_SPEAKING_PHRASES,
        FEATURE_SPEAKING_TIPS,
        FEATURE_SPEAKING_RECORD,
    }
)

SPEAKING_FEATURE_LABELS = {
    FEATURE_SPEAKING_QUESTIONS: "Common questions",
    FEATURE_SPEAKING_PRONUNCIATION: "Pronunciation",
    FEATURE_SPEAKING_PHRASES: "Useful phrases",
    FEATURE_SPEAKING_TIPS: "Speaking tips",
    FEATURE_SPEAKING_RECORD: "Practice recording",
}

READING_PREMIUM_FEATURES = frozenset(
    {
        FEATURE_READING_QUESTION_TYPES,
        FEATURE_READING_STRATEGIES,
    }
)

READING_FEATURE_LABELS = {
    FEATURE_READING_QUESTION_TYPES: "Question types",
    FEATURE_READING_STRATEGIES: "Strategies & time plan",
}

LISTENING_PREMIUM_FEATURES = frozenset(
    {
        FEATURE_LISTENING_GAP_FILL,
        FEATURE_LISTENING_SENTENCE,
        FEATURE_LISTENING_MATCHING,
        FEATURE_LISTENING_MAP,
        FEATURE_LISTENING_SHORT_ANSWER,
        FEATURE_LISTENING_SECTION4,
        FEATURE_LISTENING_DETAIL_DRILLS,
    }
)

LISTENING_FEATURE_LABELS = {
    FEATURE_LISTENING_MULTIPLE_CHOICE: "Multiple choice",
    FEATURE_LISTENING_GAP_FILL: "Form, note & table completion",
    FEATURE_LISTENING_SENTENCE: "Sentence completion",
    FEATURE_LISTENING_MATCHING: "Matching",
    FEATURE_LISTENING_MAP: "Map, plan & diagram labelling",
    FEATURE_LISTENING_SHORT_ANSWER: "Short-answer questions",
    FEATURE_LISTENING_SECTION4: "Section 4 note-taking",
    FEATURE_LISTENING_DETAIL_DRILLS: "Numbers, dates & spelling",
}

LISTENING_QTYPE_FEATURES = {
    "multiple-choice": FEATURE_LISTENING_MULTIPLE_CHOICE,
    "gap-fill": FEATURE_LISTENING_GAP_FILL,
    "sentence": FEATURE_LISTENING_SENTENCE,
    "matching": FEATURE_LISTENING_MATCHING,
    "map": FEATURE_LISTENING_MAP,
    "short-answer": FEATURE_LISTENING_SHORT_ANSWER,
}


def writing_task1_attempt_count(user) -> int:
    from writing.models import WritingTask1Attempt

    return WritingTask1Attempt.objects.filter(user=user).count()


def writing_task2_attempt_count(user) -> int:
    from writing.models import WritingTask2Attempt

    return WritingTask2Attempt.objects.filter(user=user).count()


def user_can(user, feature: str, **kwargs) -> bool:
    """Return whether the user's plan may use a gated feature."""
    if not user or not user.is_authenticated:
        return False
    if not is_free_plan(user):
        return True

    if feature == FEATURE_PRACTICE_TEST:
        test_number = int(kwargs.get("test_number", 1))
        return test_number <= FREE_PRACTICE_TEST_MAX
    if feature == FEATURE_ACADEMIC_READING:
        test_number = int(kwargs.get("test_number", 1))
        return test_number <= FREE_ACADEMIC_READING_MAX
    if feature == FEATURE_VOCAB_FLASHCARDS:
        return True
    if feature in VOCAB_PREMIUM_FEATURES:
        return False
    if feature == FEATURE_WRITING_TASK1:
        return writing_task1_attempt_count(user) < FREE_WRITING_TASK_ATTEMPTS
    if feature == FEATURE_WRITING_TASK2:
        return writing_task2_attempt_count(user) < FREE_WRITING_TASK_ATTEMPTS
    if feature in WRITING_PREMIUM_FEATURES:
        return False
    if feature in SPEAKING_PREMIUM_FEATURES:
        return False
    if feature in READING_PREMIUM_FEATURES:
        return False
    if feature == FEATURE_LISTENING_MULTIPLE_CHOICE:
        return True
    if feature in LISTENING_PREMIUM_FEATURES:
        return False
    return True


def lock_message_for(feature: str, **kwargs) -> str:
    if feature == FEATURE_PRACTICE_TEST:
        return PRACTICE_TEST_LOCK_MSG
    if feature == FEATURE_ACADEMIC_READING:
        return ACADEMIC_READING_LOCK_MSG
    if feature in VOCAB_PREMIUM_FEATURES:
        label = VOCAB_FEATURE_LABELS.get(feature, "This study method")
        return f"{label} is {VOCAB_PREMIUM_LOCK_MSG.lower()}."
    if feature == FEATURE_WRITING_TASK1:
        return f"Academic Task 1 — {WRITING_TASK_USED_MSG.lower()} on the free plan."
    if feature == FEATURE_WRITING_TASK2:
        return f"Academic Task 2 — {WRITING_TASK_USED_MSG.lower()} on the free plan."
    if feature in WRITING_PREMIUM_FEATURES:
        label = WRITING_FEATURE_LABELS.get(feature, "This section")
        return f"{label} is {VOCAB_PREMIUM_LOCK_MSG.lower()}."
    if feature in SPEAKING_PREMIUM_FEATURES:
        label = SPEAKING_FEATURE_LABELS.get(feature, "Speaking study")
        return f"{label} is {VOCAB_PREMIUM_LOCK_MSG.lower()}."
    if feature in READING_PREMIUM_FEATURES:
        label = READING_FEATURE_LABELS.get(feature, "This section")
        return f"{label} is {VOCAB_PREMIUM_LOCK_MSG.lower()}."
    if feature == FEATURE_LISTENING_MULTIPLE_CHOICE or feature in LISTENING_PREMIUM_FEATURES:
        label = LISTENING_FEATURE_LABELS.get(feature, "This listening type")
        return f"{label} is {VOCAB_PREMIUM_LOCK_MSG.lower()}."
    return VOCAB_PREMIUM_LOCK_MSG


def _redirect_for_feature(feature: str):
    from django.shortcuts import redirect

    if feature.startswith("vocab_"):
        return redirect("vocabulary:home")
    if feature in WRITING_PREMIUM_FEATURES or feature in (
        FEATURE_WRITING_TASK1,
        FEATURE_WRITING_TASK2,
    ):
        return redirect("writing:home")
    if feature in SPEAKING_PREMIUM_FEATURES:
        return redirect("home")
    if feature in READING_PREMIUM_FEATURES:
        return redirect("reading:home")
    if feature == FEATURE_LISTENING_MULTIPLE_CHOICE or feature in LISTENING_PREMIUM_FEATURES:
        return redirect("listening:home")
    if feature == FEATURE_PRACTICE_TEST:
        return redirect("practice_test:tests")
    if feature == FEATURE_ACADEMIC_READING:
        return redirect("reading:academic_tests_index")
    return redirect("home")


def guard_feature(request, feature: str, *, json_response: bool = False, **kwargs):
    """Block access when the plan disallows a feature. Returns a response or None."""
    if user_can(request.user, feature, **kwargs):
        return None
    message = lock_message_for(feature, **kwargs)
    if json_response:
        from django.http import JsonResponse

        return JsonResponse(
            {"ok": False, "error": "plan_locked", "message": message},
            status=403,
        )
    from django.contrib import messages

    messages.warning(request, message)
    return _redirect_for_feature(feature)


def guard_ai_check(user, feature: str, *, will_call_openai: bool = True) -> str | None:
    """Consume one AI check if allowed. Returns error message when blocked."""
    allowed, msg = consume_ai_check(user, feature, will_call_openai=will_call_openai)
    return msg if not allowed else None


def ai_limit_json():
    from django.http import JsonResponse

    return JsonResponse({"ok": False, "error": "ai_limit", "message": AI_LIMIT_MSG}, status=429)


def deny_practice_test_redirect(request, test_number: int):
    return guard_feature(
        request, FEATURE_PRACTICE_TEST, test_number=test_number
    )


def deny_academic_reading_redirect(request, test_number: int):
    return guard_feature(
        request, FEATURE_ACADEMIC_READING, test_number=test_number
    )


def istanbul_today():
    from django.utils import timezone

    return timezone.now().astimezone(IST).date()


def get_user_plan(user) -> str:
    if not user or not user.is_authenticated:
        return PLAN_FREE
    from vocabulary.models import UserProfile

    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return (profile.plan or PLAN_FREE).strip().lower() or PLAN_FREE


def is_free_plan(user) -> bool:
    return get_user_plan(user) == PLAN_FREE


def can_access_practice_test(user, test_number: int) -> bool:
    return user_can(user, FEATURE_PRACTICE_TEST, test_number=test_number)


def can_access_academic_reading(user, test_number: int) -> bool:
    return user_can(user, FEATURE_ACADEMIC_READING, test_number=test_number)


def _daily_limit(user) -> int | None:
    if not is_free_plan(user):
        return None
    return getattr(settings, "FREE_DAILY_AI_LIMIT", FREE_DAILY_AI_LIMIT)


def get_ai_usage(user) -> dict:
    """Return usage summary for templates and JS."""
    limit = _daily_limit(user)
    if limit is None:
        return {
            "limited": False,
            "limit": None,
            "used": 0,
            "remaining": None,
            "at_limit": False,
            "label": "",
            "limit_message": "",
        }

    from vocabulary.models import DailyAiUsage

    today = istanbul_today()
    row = DailyAiUsage.objects.filter(user=user, usage_date=today).first()
    used = row.count if row else 0
    remaining = max(0, limit - used)
    at_limit = remaining <= 0
    return {
        "limited": True,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "at_limit": at_limit,
        "label": f"{remaining} of {limit} checks left today",
        "limit_message": AI_LIMIT_MSG,
    }


@transaction.atomic
def consume_ai_check(user, feature: str, *, will_call_openai: bool = True) -> tuple[bool, str | None]:
    """Reserve one AI check. Returns (allowed, error_message)."""
    if not will_call_openai:
        return True, None

    from vocabulary.models import AiUsageLog, DailyAiUsage

    limit = _daily_limit(user)
    if limit is not None:
        today = istanbul_today()
        row, _ = DailyAiUsage.objects.select_for_update().get_or_create(
            user=user,
            usage_date=today,
            defaults={"count": 0},
        )
        if row.count >= limit:
            return False, AI_LIMIT_MSG
        DailyAiUsage.objects.filter(pk=row.pk).update(count=F("count") + 1)

    AiUsageLog.objects.create(user=user, feature=feature)
    return True, None


def plan_context_for_user(user) -> dict:
    if not user or not user.is_authenticated:
        return {}
    plan = get_user_plan(user)
    ai = get_ai_usage(user)
    return {
        "user_plan": plan,
        "is_free_plan": plan == PLAN_FREE,
        "plan_ai": ai,
        "plan_practice_test_max": FREE_PRACTICE_TEST_MAX if plan == PLAN_FREE else None,
        "plan_academic_reading_max": FREE_ACADEMIC_READING_MAX if plan == PLAN_FREE else None,
        "practice_test_lock_message": PRACTICE_TEST_LOCK_MSG,
        "academic_reading_lock_message": ACADEMIC_READING_LOCK_MSG,
        "vocab_premium_lock_message": VOCAB_PREMIUM_LOCK_MSG,
        "writing_task_used_message": WRITING_TASK_USED_MSG,
        "writing_free_attempt_note": WRITING_FREE_ATTEMPT_NOTE,
        "writing_task1_can_submit": user_can(user, FEATURE_WRITING_TASK1),
        "writing_task2_can_submit": user_can(user, FEATURE_WRITING_TASK2),
    }
