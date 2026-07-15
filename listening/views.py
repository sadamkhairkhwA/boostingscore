import json
import re

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.templatetags.static import static

from boostingscore.plan_limits import (
    FEATURE_LISTENING_DETAIL_DRILLS,
    FEATURE_LISTENING_SECTION4,
    LISTENING_QTYPE_FEATURES,
    guard_feature,
)

from .cycle_service import mark_set_completed, pick_random_set
from .models import ListeningPracticeAttempt
from .practice_data import (
    PRACTICE_SETS,
    TYPE_LABELS,
    get_set,
    get_sets,
    get_types,
    uses_type_hub,
)
from .tip_icons import TYPE_SET_ICONS, TYPE_TIP_ICONS
from .tips_content import GENERAL_TIPS, TYPE_TIPS


def _guard_listening_qtype(request, qtype: str):
    feature = LISTENING_QTYPE_FEATURES.get(qtype)
    if not feature:
        return None
    return guard_feature(request, feature)


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


def _annotate_sets(sets: list[dict]) -> list[dict]:
    """Attach audio_ready flag for templates."""
    out = []
    for s in sets:
        item = dict(s)
        item["audio_ready"] = _audio_exists(s.get("audio", ""))
        out.append(item)
    return out


def _best_scores(user, qtype: str, set_ids: list[str]) -> dict[str, dict]:
    """Best percent per set_id for this user and question type."""
    if not set_ids:
        return {}
    attempts = (
        ListeningPracticeAttempt.objects.filter(
            student=user,
            question_type=qtype,
            set_id__in=set_ids,
        )
        .order_by("set_id", "-score", "-created_at")
    )
    best: dict[str, dict] = {}
    for a in attempts:
        if a.set_id in best:
            continue
        best[a.set_id] = {"score": a.score, "total": a.total, "percent": a.percent}
    return best


def _enrich_tips(qtype: str, tips: dict) -> dict:
    """Attach icon slug and number to each tip (content unchanged)."""
    data = dict(tips)
    icons = TYPE_TIP_ICONS.get(qtype, [])
    enriched = []
    for i, tip in enumerate(data.get("tips") or []):
        row = dict(tip)
        row["number"] = i + 1
        row["icon"] = icons[i] if i < len(icons) else "lightbulb"
        enriched.append(row)
    data["tips"] = enriched
    return data


def _set_card_icon(qtype: str, s: dict, index: int) -> str:
    icons = TYPE_SET_ICONS.get(qtype, [])
    if icons and index < len(icons):
        return icons[index]
    return "headphones"


def _recent_attempts(user, limit: int = 6) -> list[ListeningPracticeAttempt]:
    """One recent row per set, keeping the best score and latest tie-break."""
    attempts = (
        ListeningPracticeAttempt.objects.filter(student=user)
        .order_by("question_type", "set_id", "-score", "-created_at")
    )
    best_by_set: dict[tuple[str, str], ListeningPracticeAttempt] = {}
    for attempt in attempts:
        key = (attempt.question_type, attempt.set_id)
        if key in best_by_set:
            continue
        best_by_set[key] = attempt
    rows = sorted(best_by_set.values(), key=lambda a: a.created_at, reverse=True)
    return rows[:limit]


# --------------------------------------------------------------------------- #
#  Views
# --------------------------------------------------------------------------- #
@login_required
def listening_home(request):
    recent = _recent_attempts(request.user)
    types = get_types()
    for t in types:
        t["plan_feature"] = LISTENING_QTYPE_FEATURES.get(t["slug"], "")
    return render(
        request,
        "listening/home.html",
        {
            "types": types,
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


def _prepare_sets(request, qtype: str) -> list[dict]:
    sets = _annotate_sets(get_sets(qtype))
    set_ids = [s["id"] for s in sets]
    best = _best_scores(request.user, qtype, set_ids)
    for i, s in enumerate(sets):
        s["best_score"] = best.get(s["id"])
        s["icon"] = _set_card_icon(qtype, s, i)
    return sets


@login_required
def type_detail(request, qtype):
    if qtype not in PRACTICE_SETS:
        raise Http404("Unknown listening question type.")
    blocked = _guard_listening_qtype(request, qtype)
    if blocked:
        return blocked

    type_label = TYPE_LABELS.get(qtype, qtype)
    raw_tips = TYPE_TIPS.get(qtype)
    if not raw_tips:
        raise Http404("Tips not available for this type.")
    tips = _enrich_tips(qtype, raw_tips)

    return render(
        request,
        "listening/type_detail.html",
        {
            "qtype": qtype,
            "type_label": type_label,
            "tips": tips,
        },
    )


@login_required
def type_tests(request, qtype):
    """Legacy URL — send students straight into random practice."""
    if qtype not in PRACTICE_SETS:
        raise Http404("Unknown listening question type.")
    blocked = _guard_listening_qtype(request, qtype)
    if blocked:
        return blocked
    return redirect("listening:practice", qtype=qtype)


@login_required
def practice(request, qtype):
    if qtype not in PRACTICE_SETS:
        raise Http404("Unknown listening question type.")
    blocked = _guard_listening_qtype(request, qtype)
    if blocked:
        return blocked

    set_id = request.GET.get("set") or request.POST.get("set_id")
    type_label = TYPE_LABELS.get(qtype, qtype)
    use_hub = uses_type_hub(qtype)
    tips_url = reverse("listening:type_detail", kwargs={"qtype": qtype})
    hub_url = tips_url if use_hub else reverse("listening:home")

    if use_hub and not set_id and request.method == "GET":
        picked = pick_random_set(request.user, qtype, _audio_exists)
        if not picked:
            raise Http404("No practice audio available for this type yet.")
        return redirect(f"{reverse('listening:practice', kwargs={'qtype': qtype})}?set={picked['id']}")

    pset = get_set(qtype, set_id)
    if not pset:
        raise Http404("No practice set available for this type yet.")

    questions = pset["questions"]

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

        cycle_result = None
        if use_hub:
            cycle_result = mark_set_completed(
                request.user, qtype, pset["id"], _audio_exists
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
                "hub_url": hub_url,
                "show_test_hub": use_hub,
                "cycle_complete": cycle_result and cycle_result["cycle_complete"],
                "cycle_total": cycle_result["total"] if cycle_result else 0,
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
            "hub_url": hub_url,
            "show_test_hub": use_hub,
        },
    )


def _norm_detail(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("£", "").replace("$", "")
    s = re.sub(r"[.,;:!?\"'`]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


@login_required
def section4_notes_index(request):
    blocked = guard_feature(request, FEATURE_LISTENING_SECTION4)
    if blocked:
        return blocked
    from .section4_notes_content import SECTION4_NOTE_LECTURES

    lectures = []
    for lec in SECTION4_NOTE_LECTURES:
        item = dict(lec)
        item["audio_ready"] = _audio_exists(lec.get("audio", ""))
        lectures.append(item)
    return render(
        request,
        "listening/section4_notes_index.html",
        {"lectures": lectures},
    )


@login_required
def section4_notes_session(request, lecture_id: str):
    blocked = guard_feature(request, FEATURE_LISTENING_SECTION4)
    if blocked:
        return blocked
    from boostingscore.review_schedule import mark_section_reviewed
    from .section4_notes_content import SECTION4_NOTE_LECTURES

    lecture = next((l for l in SECTION4_NOTE_LECTURES if l["id"] == lecture_id), None)
    if not lecture:
        raise Http404

    if request.method == "POST":
        mark_section_reviewed(request.user, "listening_notes")
        answers = {k: v for k, v in request.POST.items() if k.startswith("gap_")}
        results = []
        score = 0
        for field in lecture["template"]:
            fid = field["id"]
            given = answers.get(f"gap_{fid}", "")
            correct = field["answer"]
            ok = _norm_detail(given) == _norm_detail(correct)
            if ok:
                score += 1
            results.append(
                {
                    "id": fid,
                    "label": field["label"],
                    "given": given,
                    "correct": correct,
                    "ok": ok,
                }
            )
        total = len(lecture["template"])
        ListeningPracticeAttempt.objects.create(
            student=request.user,
            question_type="section4-notes",
            type_label="Section 4 notes",
            set_id=lecture["id"],
            set_title=lecture["title"],
            score=score,
            total=total,
            answers_json=answers,
        )
        return render(
            request,
            "listening/section4_notes_session.html",
            {
                "lecture": lecture,
                "mode": "results",
                "results": results,
                "score": score,
                "total": total,
                "percent": round(score / total * 100) if total else 0,
                "audio_url": _audio_url(lecture["audio"]),
                "audio_missing": not _audio_exists(lecture["audio"]),
            },
        )

    mark_section_reviewed(request.user, "listening_notes")
    return render(
        request,
        "listening/section4_notes_session.html",
        {
            "lecture": lecture,
            "mode": "play",
            "audio_url": _audio_url(lecture["audio"]),
            "audio_missing": not _audio_exists(lecture["audio"]),
        },
    )


@login_required
def detail_drills(request):
    blocked = guard_feature(request, FEATURE_LISTENING_DETAIL_DRILLS)
    if blocked:
        return blocked
    from boostingscore.review_schedule import mark_section_reviewed
    from .detail_drills_content import DETAIL_DRILLS, DRILL_TYPE_LABELS

    mark_section_reviewed(request.user, "listening_details")
    drills = []
    for d in DETAIL_DRILLS:
        item = dict(d)
        item["audio_ready"] = _audio_exists(d.get("audio", ""))
        item["audio_url"] = _audio_url(d["audio"])
        drills.append(item)
    return render(
        request,
        "listening/detail_drills.html",
        {
            "drills": drills,
            "drills_json": json.dumps(drills),
            "type_labels": DRILL_TYPE_LABELS,
        },
    )
