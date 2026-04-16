import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import IELTSTest, IELTSTestContent, IELTSTestResult


def get_streak(user):
    return getattr(getattr(user, "profile", None), "streak", 0) or 0


@login_required
def reading_home(request):
    user = request.user
    streak = 0
    try:
        streak = int(getattr(getattr(user, "profile", None), "streak", 0) or 0)
    except Exception:
        streak = 0

    best_streak = 0
    try:
        best_streak = int(getattr(getattr(user, "profile", None), "best_streak", 0) or 0)
    except Exception:
        best_streak = 0

    sessions = 0
    avg_score = None
    tests_done = 0
    ielts_avg = None
    passages_read = 0
    passage_avg = None
    in_progress = 0

    try:
        all_results = IELTSTestResult.objects.filter(student=user)
        sessions = all_results.count()
        tests_done = sessions
        scores = []
        try:
            scores = [float(r.score) for r in all_results]
        except Exception:
            scores = []
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)
        if scores:
            ielts_avg = avg_score
    except Exception:
        pass

    try:
        passages_read = int(request.session.get("reading_quiz_completions", 0) or 0)
    except Exception:
        passages_read = 0

    try:
        passage_avg = avg_score
    except Exception:
        passage_avg = None

    try:
        in_progress = int(request.session.get("reading_in_progress", 0) or 0)
    except Exception:
        in_progress = 0

    tests = IELTSTest.objects.order_by("test_number")
    return render(
        request,
        "reading/reading_home.html",
        {
            "tests": [
                {
                    "id": t.test_number,
                    "title": t.topic,
                    "band": t.band_range,
                    "types": t.question_types,
                    "desc": t.description or "",
                    "available": bool(t.is_active and t.is_published),
                    "pk": t.pk,
                }
                for t in tests
            ],
            "streak": streak,
            "best_streak": best_streak,
            "sessions": sessions,
            "sessions_done": sessions,
            "avg_score": avg_score,
            "overall_avg": avg_score,
            "tests_done": tests_done,
            "ielts_done": tests_done,
            "ielts_avg": ielts_avg,
            "passages_read": passages_read,
            "passage_avg": passage_avg,
            "in_progress": in_progress,
        },
    )


@login_required
def ielts_practice(request):
    tests = IELTSTest.objects.filter(
        is_active=True,
        is_published=True,
    ).order_by("test_number")
    tests_data = [
        {
            "id": t.pk,
            "test_number": t.test_number,
            "topic": t.topic,
            "band_range": t.band_range,
            "difficulty": t.get_difficulty_display(),
            "question_types": t.question_types,
            "description": t.description,
            "total_questions": t.total_questions,
            "time_limit": t.time_limit,
        }
        for t in tests
    ]
    return render(
        request,
        "reading/ielts_test_list.html",
        {
            "streak": get_streak(request.user),
            "tests_data": tests_data,
        },
    )


@login_required
@csrf_exempt
def generate_ielts_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
        test_id = int(payload.get("test_id") or 0)
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({"error": "Invalid request body"}, status=400)

    test = get_object_or_404(
        IELTSTest,
        id=test_id,
        is_published=True,
        is_active=True,
    )
    content_row = test.contents.filter(is_current=True).order_by("-version").first()
    if not content_row:
        return JsonResponse({"error": "This test has no current content."}, status=404)
    return JsonResponse({"success": True, "test": content_row.content_json})


@login_required
@csrf_exempt
def submit_ielts_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        score = int(data.get("score", 0))
        total = int(data.get("total", 40))
        time_secs = int(data.get("time_secs", 0))
        answers = data.get("answers", {})
        test_id = int(data.get("test_id", 0))
        test = get_object_or_404(IELTSTest, id=test_id)

        IELTSTestResult.objects.create(
            student=request.user,
            test=test,
            score=score,
            total_questions=total,
            time_seconds=time_secs,
            answers_json=answers,
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def ielts_exam(request, test_id: int):
    test = get_object_or_404(
        IELTSTest,
        id=test_id,
        is_published=True,
        is_active=True,
    )
    if not test.contents.filter(is_current=True).exists():
        messages.error(
            request,
            "This test has no content yet. Please check back soon.",
        )
        return redirect("reading:ielts_practice")
    return render(
        request,
        "reading/ielts_exam.html",
        {
            "test": test,
            "streak": get_streak(request.user),
            "candidate_name": request.user.first_name or request.user.username,
        },
    )


# Backward-compatible alias for existing URL names.
ielts_home = ielts_practice


@login_required
def strategies(request):
    strategies_data = [
        {
            "title": "Don't read the whole passage first",
            "points": [
                "Wastes 5–10 minutes",
                "Go to questions first",
                "Passage is a reference, not a story",
            ],
            "tag": "Common mistake",
            "tag_tone": "rose",
        },
        {
            "title": "Reading = finding answers, not understanding everything",
            "points": [
                "You don't need to understand every word",
                "Just locate correct information fast",
                "Skip any paragraph with no question",
            ],
            "tag": "Mindset shift",
            "tag_tone": "green",
        },
        {
            "title": "Use keywords from the question",
            "points": [
                "Find important words in the question first",
                "Names, numbers, dates work best",
                "Then scan the passage for those words",
            ],
            "tag": "Technique",
            "tag_tone": "blue",
        },
        {
            "title": "Look for synonyms — IELTS always changes the words",
            "points": [
                "Same meaning does not mean same words",
                "injured in question = hurt in passage",
                "Build your synonym vocabulary",
            ],
            "tag": "Critical",
            "tag_tone": "blue",
        },
        {
            "title": "Answer questions in order",
            "points": [
                "Answers appear top to bottom in passage",
                "Matches the order of questions",
                "Never re-read sections already passed",
            ],
            "tag": "Time saver",
            "tag_tone": "green",
        },
        {
            "title": "Don't panic — skip and move on",
            "points": [
                "Mark hard questions and move forward",
                "One hard question is not worth three easy ones",
                "Come back if time allows",
            ],
            "tag": "Stay calm",
            "tag_tone": "amber",
        },
        {
            "title": "Time management is critical",
            "points": [
                "Max 2 minutes per question",
                "No penalty for wrong answers in IELTS",
                "Never leave a question blank — always guess",
            ],
            "tag": "Critical",
            "tag_tone": "rose",
        },
        {
            "title": "Check answers at the end",
            "points": [
                "Focus on TF/NG and Yes/No/NG first",
                "One word changes everything",
                "If you used strategies 1–7 you will have time",
            ],
            "tag": "Bonus",
            "tag_tone": "blue",
        },
    ]
    return render(
        request,
        "reading/strategies.html",
        {
            "streak": get_streak(request.user),
            "strategies": strategies_data,
        },
    )


@login_required
def skills(request):
    return render(
        request,
        "reading/skills.html",
        {
            "streak": get_streak(request.user),
        },
    )


@login_required
def general_reading(request):
    return render(
        request,
        "reading/general_reading.html",
        {
            "streak": get_streak(request.user),
        },
    )
