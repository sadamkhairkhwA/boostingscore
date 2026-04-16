import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from vocabulary.models import Word

from .models import UserProfile
from .placement_data import PLACEMENT_QUESTIONS

SESSION_TEST = "placement_test_questions"
SESSION_ANSWERS = "placement_answers"

PLACEMENT_COUNT = 20


def _build_questions_from_words() -> list[dict]:
    pool = list(
        Word.objects.exclude(word="")
        .exclude(definition="")
        .exclude(definition__isnull=True)
    )
    random.shuffle(pool)
    out: list[dict] = []
    for w in pool:
        if len((w.definition or "").strip()) < 8:
            continue
        others = [x for x in pool if x.pk != w.pk]
        random.shuffle(others)
        distr: list[str] = []
        seen = {(w.word or "").strip().lower()}
        for x in others:
            t = (x.word or "").strip()
            if not t or t.lower() in seen:
                continue
            seen.add(t.lower())
            distr.append(t)
            if len(distr) >= 3:
                break
        if len(distr) < 3:
            continue
        answer = (w.word or "").strip()
        opts = [answer] + distr[:3]
        random.shuffle(opts)
        try:
            correct = opts.index(answer)
        except ValueError:
            continue
        out.append(
            {
                "definition": (w.definition or "").strip()[:2000],
                "options": opts,
                "correct": correct,
            }
        )
        if len(out) >= PLACEMENT_COUNT:
            break

    si = 0
    while len(out) < PLACEMENT_COUNT and si < len(PLACEMENT_QUESTIONS):
        q = PLACEMENT_QUESTIONS[si]
        si += 1
        out.append(
            {
                "definition": q["prompt"],
                "options": list(q["options"]),
                "correct": int(q["correct"]),
            }
        )

    while len(out) < PLACEMENT_COUNT and PLACEMENT_QUESTIONS:
        q = PLACEMENT_QUESTIONS[len(out) % len(PLACEMENT_QUESTIONS)]
        out.append(
            {
                "definition": q["prompt"],
                "options": list(q["options"]),
                "correct": int(q["correct"]),
            }
        )

    return out[:PLACEMENT_COUNT]


@login_required
def placement_start(request):
    questions = _build_questions_from_words()
    if len(questions) < PLACEMENT_COUNT:
        questions = [
            {
                "definition": q["prompt"],
                "options": list(q["options"]),
                "correct": int(q["correct"]),
            }
            for q in PLACEMENT_QUESTIONS[:PLACEMENT_COUNT]
        ]
    request.session[SESSION_TEST] = questions
    request.session[SESSION_ANSWERS] = [None] * len(questions)
    request.session.modified = True
    return redirect("placement:question", n=0)


@login_required
def placement_question(request, n: int):
    questions = request.session.get(SESSION_TEST) or []
    n = int(n)
    if not questions or n < 0 or n >= len(questions):
        return redirect("placement:start")

    answers = request.session.get(SESSION_ANSWERS)
    if answers is None or len(answers) != len(questions):
        if request.method == "GET":
            return redirect("placement:start")
        answers = [None] * len(questions)

    if request.method == "POST":
        choice = request.POST.get("choice")
        if choice is not None and choice.isdigit():
            answers[n] = int(choice)
        request.session[SESSION_ANSWERS] = answers
        request.session.modified = True
        if n >= len(questions) - 1:
            return redirect("placement:results")
        return redirect("placement:question", n=n + 1)

    q = questions[n]
    return render(
        request,
        "placement/question.html",
        {
            "index": n,
            "total": len(questions),
            "q": q,
        },
    )


@login_required
def placement_results(request):
    questions = request.session.get(SESSION_TEST) or []
    answers = request.session.get(SESSION_ANSWERS) or []
    if (
        not questions
        or len(answers) != len(questions)
        or any(a is None for a in answers)
    ):
        return redirect("placement:start")

    correct = sum(
        1 for i, a in enumerate(answers) if a == questions[i]["correct"]
    )
    total = len(questions)
    pct = round(100.0 * correct / total) if total else 0

    if pct <= 40:
        level = 1
        level_name = "Beginner"
    elif pct <= 70:
        level = 2
        level_name = "Standard"
    else:
        level = 3
        level_name = "Advanced"

    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"level": level, "placement_completed": True},
    )
    profile.level = level
    profile.placement_completed = True
    profile.save(update_fields=["level", "placement_completed"])

    request.session.pop(SESSION_TEST, None)
    request.session.pop(SESSION_ANSWERS, None)
    request.session.modified = True

    return render(
        request,
        "placement/results.html",
        {
            "correct": correct,
            "total": total,
            "percent": pct,
            "level": level,
            "level_name": level_name,
        },
    )


@login_required
def placement_retake_prepare(request):
    """Clear placement gate so middleware sends user through the test again."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.placement_completed = False
    profile.save(update_fields=["placement_completed"])
    request.session.pop(SESSION_TEST, None)
    request.session.pop(SESSION_ANSWERS, None)
    request.session.modified = True
    return redirect("placement:start")
