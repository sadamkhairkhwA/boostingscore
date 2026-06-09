import re

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.templatetags.static import static

from .models import ListeningPracticeAttempt
from .practice_data import PRACTICE_SETS, TYPE_LABELS, get_set, get_types
from .tips_content import GENERAL_TIPS, TYPE_TIPS


# --------------------------------------------------------------------------- #
#  Grading helpers
# --------------------------------------------------------------------------- #
def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("£", "").replace("$", "")
    s = re.sub(r"[.,;:!?\"'`]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _is_correct(question: dict, given: str) -> bool:
    answer = question.get("answer")
    if question.get("render") in ("radio", "select"):
        return (given or "").strip() == str(answer).strip()
    accepted = answer if isinstance(answer, list) else [answer]
    g = _norm(given)
    if not g:
        return False
    return any(_norm(str(a)) == g for a in accepted)


def _display_answer(question: dict) -> str:
    answer = question.get("answer")
    if isinstance(answer, list):
        return str(answer[0])
    return str(answer)


def _audio_url(filename: str) -> str:
    return static(f"listening_practice/{filename}")


def _audio_exists(filename: str) -> bool:
    from django.contrib.staticfiles import finders

    return bool(finders.find(f"listening_practice/{filename}"))


# --------------------------------------------------------------------------- #
#  Views
# --------------------------------------------------------------------------- #
@login_required
def listening_home(request):
    recent = ListeningPracticeAttempt.objects.filter(student=request.user)[:6]
    return render(
        request,
        "listening/home.html",
        {
            "types": get_types(),
            "recent": recent,
        },
    )


@login_required
def tips(request):
    return render(
        request,
        "listening/tips.html",
        {
            "type_tips": TYPE_TIPS,
            "general": GENERAL_TIPS,
        },
    )


@login_required
def practice(request, qtype):
    if qtype not in PRACTICE_SETS:
        raise Http404("Unknown listening question type.")

    set_id = request.GET.get("set") or request.POST.get("set_id")
    pset = get_set(qtype, set_id)
    if not pset:
        raise Http404("No practice set available for this type yet.")

    questions = pset["questions"]
    type_label = TYPE_LABELS.get(qtype, qtype)

    if request.method == "POST":
        results = []
        score = 0
        given_map = {}
        for i, q in enumerate(questions, start=1):
            given = (request.POST.get(q["id"]) or "").strip()
            given_map[q["id"]] = given
            ok = _is_correct(q, given)
            if ok:
                score += 1
            results.append({
                "number": i,
                "text": q["text"],
                "render": q["render"],
                "given": given,
                "correct": ok,
                "correct_answer": _display_answer(q),
                "explanation": q.get("explanation", ""),
            })

        ListeningPracticeAttempt.objects.create(
            student=request.user,
            question_type=qtype,
            type_label=type_label,
            set_id=pset["id"],
            set_title=pset.get("title", ""),
            score=score,
            total=len(questions),
            answers_json=given_map,
        )

        return render(
            request,
            "listening/practice.html",
            {
                "qtype": qtype,
                "type_label": type_label,
                "pset": pset,
                "mode": "results",
                "results": results,
                "score": score,
                "total": len(questions),
                "percent": round(score / len(questions) * 100) if questions else 0,
            },
        )

    # GET — render the player + questions.
    numbered = [dict(q, number=i) for i, q in enumerate(questions, start=1)]
    return render(
        request,
        "listening/practice.html",
        {
            "qtype": qtype,
            "type_label": type_label,
            "pset": pset,
            "questions": numbered,
            "audio_url": _audio_url(pset["audio"]),
            "audio_missing": not _audio_exists(pset["audio"]),
            "mode": "play",
            "total": len(questions),
        },
    )
