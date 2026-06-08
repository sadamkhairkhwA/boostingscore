from __future__ import annotations

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST

from . import content as C
from . import listening_content as LC
from . import tts
from .models import SpeakingResponse, TestSession
from .scoring import (
    _annotate_response,
    _compute_speaking_metrics,
    annotate_speaking_transcript,
    reading_band_from_correct,
    round_half,
    score_speaking,
    score_writing,
    synthesize_speaking_report,
    transcribe_audio,
)


# =============================================================================
# Hub
# =============================================================================

@login_required
def tests(request):
    """Chooser page: lists Practice Tests 1–5 as cards (active or coming soon)."""
    from . import papers
    return render(
        request,
        "practice_test/tests_chooser.html",
        {"tests": papers.list_tests()},
    )


@login_required
def enter_test(request, n: int):
    """Select a practice test, remember it for the session, open its hub."""
    from . import papers
    if not papers.is_active(n):
        return redirect("practice_test:tests")
    request.session["pt_test"] = int(n)
    return redirect("practice_test:hub")


@login_required
def hub(request):
    history = (
        TestSession.objects.filter(user=request.user)
        .exclude(status=TestSession.STATUS_IN_PROGRESS, band_overall__isnull=True)
        .order_by("-started_at")[:8]
    )
    latest = {}
    for kind, _label in TestSession.KIND_CHOICES:
        last = (
            TestSession.objects.filter(user=request.user, kind=kind, status=TestSession.STATUS_COMPLETED)
            .order_by("-completed_at")
            .first()
        )
        if last is not None:
            latest[kind] = last
    n = _active_test(request)
    passages = _reading_passages_for(n)
    ldict = _listening_dict_for(n)
    return render(
        request,
        "practice_test/hub.html",
        {
            "history": history,
            "latest": latest,
            "active_test": n,
            "is_test_one": n == 1,
            "speaking_available": n in SPEAKING_TESTS,
            "listening_available": tts.audio_exists() if n == 1 else True,
            "listening_total": sum(len(s["questions"]) for s in ldict.get("sections", [])),
            "reading_total": sum(len(p["questions"]) for p in passages),
            "speaking_total": C.speaking_total_questions(),
        },
    )


# =============================================================================
# Reading content helper (shared between standalone + full)
# =============================================================================

# --- Per-test content selection (Test 1 = shipped modules; 2–5 = registry) ---

def _active_test(request) -> int:
    """The Practice Test number the user is currently in (default 1)."""
    try:
        n = int(request.session.get("pt_test", 1))
    except (TypeError, ValueError):
        n = 1
    return n if n in (1, 2, 3, 4, 5) else 1


def _reading_passages_for(n: int):
    from . import papers
    if n == 1:
        return C.READING_PASSAGES
    bundle = papers.get_content(n)
    return (bundle or {}).get("reading") or []


def _writing_tasks_for(n: int):
    from . import papers
    if n == 1:
        return C.WRITING_TASKS
    bundle = papers.get_content(n)
    return (bundle or {}).get("writing") or C.WRITING_TASKS


def _listening_dict_for(n: int):
    from . import papers
    if n == 1:
        return LC.LISTENING_TEST
    bundle = papers.get_content(n)
    return (bundle or {}).get("listening") or {"sections": []}


def _annotated_passages(passages=None):
    """Return passages with each question carrying a running `number`."""
    if passages is None:
        passages = C.READING_PASSAGES
    n = 0
    out = []
    for p in passages:
        qs = []
        for q in p["questions"]:
            n += 1
            qs.append({**q, "number": n})
        out.append({**p, "questions": qs})
    return out


def _grade_reading(post, passages=None) -> dict:
    """Read POST data + score it against the reading answer key."""
    if passages is None:
        passages = C.READING_PASSAGES
    answers: dict[str, str] = {}
    correct = 0
    total = 0
    by_passage: list[dict] = []
    for p in passages:
        p_correct = 0
        for q in p["questions"]:
            total += 1
            raw = (post.get(q["id"]) or "").strip()
            answers[q["id"]] = raw
            if raw and _norm_answer(raw) in _acceptable_set(q):
                correct += 1
                p_correct += 1
        by_passage.append({
            "number": p["number"],
            "title": p["title"],
            "correct": p_correct,
            "total": len(p["questions"]),
        })
    band = reading_band_from_correct(correct, total)
    return {
        "band": band,
        "answers": answers,
        "correct": correct,
        "total": total,
        "by_passage": by_passage,
    }


# =============================================================================
# Writing content helper
# =============================================================================

def _wc(text: str) -> int:
    return len([w for w in (text or "").split() if w.strip()])


def _grade_writing(post, tasks=None) -> dict:
    if tasks is None:
        tasks = C.WRITING_TASKS
    t1 = (post.get("task1_response") or "").strip()
    t2 = (post.get("task2_response") or "").strip()
    t1_wc, t2_wc = _wc(t1), _wc(t2)
    fb1 = score_writing("task1", tasks["task1"]["instructions"], t1, t1_wc)
    fb2 = score_writing("task2", tasks["task2"]["instructions"], t2, t2_wc)
    b1 = float(fb1.get("band_score") or 0)
    b2 = float(fb2.get("band_score") or 0)
    # IELTS weighting: Task 2 worth twice as much as Task 1.
    band = round_half(((b1 + 2 * b2) / 3) if (b1 or b2) else 0.0)
    # Pre-render the inline-highlighted response HTML so the results template
    # can show it without any further processing.
    t1_html = _annotate_response(t1, fb1.get("annotations") or [])
    t2_html = _annotate_response(t2, fb2.get("annotations") or [])
    return {
        "band": band,
        "task1": {
            "response": t1, "word_count": t1_wc, "feedback": fb1, "band": b1,
            "annotated_html": t1_html,
        },
        "task2": {
            "response": t2, "word_count": t2_wc, "feedback": fb2, "band": b2,
            "annotated_html": t2_html,
        },
    }


# =============================================================================
# Speaking helpers (shared between standalone + full)
# =============================================================================

# Which static folder each test's examiner videos live in. The flow itself
# (order, recording, transcription, scoring) is shared from Test 1; only the
# folder — and, for some tests, the filename scheme — differs. Tests without
# their own folder fall back to Test 1.
SPEAKING_VIDEO_FOLDERS = {
    1: "speaking_videos",
    2: "speaking_videos2",
    3: "speaking_videos3",
}

# Tests that currently have a playable Speaking section.
SPEAKING_TESTS = set(SPEAKING_VIDEO_FOLDERS)


def _speaking_video_file(test_n: int, canonical: str) -> str:
    """Map a canonical flow filename to the actual file for a given test.

    Test 3's clips are named with an ``a`` prefix and a ``_1080p`` suffix
    (e.g. ``p1_q1.mp4`` -> ``ap1_q1_1080p.mp4``); all other tests use the
    canonical names directly.
    """
    if test_n == 3:
        return "a" + canonical[:-4] + "_1080p.mp4"  # strip ".mp4", re-add suffix
    return canonical

def _get_or_create_speaking_session(user):
    """Return the most recent in-progress speaking session, or create one."""
    s = (
        TestSession.objects.filter(
            user=user, kind=TestSession.KIND_SPEAKING, status=TestSession.STATUS_IN_PROGRESS
        )
        .order_by("-started_at")
        .first()
    )
    if s is None:
        s = TestSession.objects.create(user=user, kind=TestSession.KIND_SPEAKING)
    return s


def _finalise_speaking_session(session) -> float:
    """Aggregate latest responses → band → mark completed. Return overall band."""
    responses = list(SpeakingResponse.objects.filter(session=session))
    # Take most-recent per (part, q_index) so re-records replace older ones
    keep: dict[tuple[int, int], SpeakingResponse] = {}
    for r in responses:
        key = (r.part, r.question_index)
        if key not in keep or r.created_at > keep[key].created_at:
            keep[key] = r
    final = list(keep.values())
    if not final:
        return 0.0

    def avg(field: str) -> float:
        vals = [getattr(r, field) or 0 for r in final]
        return round_half(sum(vals) / len(vals)) if vals else 0.0

    band = avg("band")
    session.band_overall = band
    session.band_speaking = band
    session.status = TestSession.STATUS_COMPLETED
    session.completed_at = timezone.now()
    session.raw = {
        "fluency": avg("fluency"),
        "vocabulary": avg("vocabulary"),
        "grammar": avg("grammar"),
        "pronunciation": avg("pronunciation"),
        "answered": len(final),
        "total": C.speaking_total_questions(),
    }
    session.save()
    return band


# =============================================================================
# Listening helpers (shared between standalone + full)
# =============================================================================

def _listening_sections_with_numbers(sections=None):
    """Return sections with running question numbers + template-friendly groups.

    Each section gets:
      questions      - all questions, with a running `number`
      first_no/last_no - question-number range for the heading
      map_questions  - questions of type "map" (rendered in the map block)
      table_rows     - resolved rows for a table-completion block (cells carry
                       the question object + number, or plain text)
      flow_questions - the remaining questions, rendered as normal rows
    """
    if sections is None:
        sections = LC.LISTENING_TEST["sections"]
    out = []
    n = 0
    for s in sections:
        qs = []
        for q in s["questions"]:
            n += 1
            qs.append({**q, "number": n})
        by_id = {q["id"]: q for q in qs}

        table_ids: set[str] = set()
        table_rows = []
        table = s.get("table")
        if table:
            for row in table["rows"]:
                cells = []
                for cell in row:
                    if "q" in cell:
                        q = by_id.get(cell["q"])
                        if q:
                            table_ids.add(q["id"])
                        cells.append({
                            "question": q,
                            "prefix": cell.get("prefix", ""),
                            "suffix": cell.get("suffix", ""),
                        })
                    else:
                        cells.append({"text": cell.get("text", "")})
                table_rows.append(cells)

        map_questions = [q for q in qs if q.get("type") == "map"]
        flow_questions = [
            q for q in qs
            if q.get("type") != "map" and q["id"] not in table_ids
        ]

        out.append({
            **s,
            "questions": qs,
            "first_no": qs[0]["number"] if qs else 0,
            "last_no": qs[-1]["number"] if qs else 0,
            "map_questions": map_questions,
            "table_rows": table_rows,
            "flow_questions": flow_questions,
        })
    return out


import re as _re


def _norm_answer(value: str) -> str:
    """Normalise an answer for tolerant comparison (case, spacing, £, times)."""
    v = (value or "").strip().lower()
    v = v.replace("£", "").replace("$", "")
    v = v.replace(".", ":") if _re.fullmatch(r"\d{1,2}\.\d{2}", v) else v  # 7.30 -> 7:30
    v = v.rstrip(".")
    v = _re.sub(r"\s+", " ", v)
    return v.strip()


def _acceptable_set(q: dict) -> set[str]:
    """Build the set of normalised acceptable answers for a question."""
    out: set[str] = set()
    ans = q.get("answer")
    values = ans if isinstance(ans, (list, tuple)) else [ans]
    for v in list(values) + list(q.get("accept", [])):
        if v is None:
            continue
        out.add(_norm_answer(str(v)))
        # For matching/map, also accept just the leading option letter (e.g. "C").
        m = _re.match(r"\s*([a-z])\b", str(v).lower())
        if q.get("type") in ("matching", "map") and m:
            out.add(m.group(1))
    return {x for x in out if x}


def _grade_listening(post, sections=None) -> dict:
    """Score POST data against the listening answer key."""
    if sections is None:
        sections = LC.LISTENING_TEST["sections"]
    answers: dict[str, str] = {}
    correct = 0
    total = 0
    by_section: list[dict] = []
    for s in sections:
        s_correct = 0
        for q in s["questions"]:
            total += 1
            raw = (post.get(q["id"]) or "").strip()
            answers[q["id"]] = raw
            if not raw:
                continue
            qtype = q.get("type")
            if qtype == "short":
                got = _norm_answer(raw)
                if any(_norm_answer(kw) in got for kw in q.get("answer_keywords", [])):
                    correct += 1
                    s_correct += 1
            else:
                got = _norm_answer(raw)
                if got in _acceptable_set(q) or any(
                    got == a or got.lstrip("0") == a.lstrip("0")
                    for a in _acceptable_set(q)
                ):
                    correct += 1
                    s_correct += 1
        by_section.append({
            "number": s["number"],
            "title":  s["title"],
            "correct": s_correct,
            "total": len(s["questions"]),
        })
    # IELTS listening uses the same raw-to-band table as Academic Reading.
    band = reading_band_from_correct(correct, total)
    return {
        "band": band,
        "answers": answers,
        "correct": correct,
        "total": total,
        "by_section": by_section,
    }


# =============================================================================
# Standalone single-section practice (no shared state with the full test)
# =============================================================================

# =============================================================================
# Exam intro / "Start exam" screens (real IELTS-style instructions per section)
# =============================================================================

EXAM_INTROS = {
    "listening": {
        "name": "Listening",
        "accent": "navy",
        "duration": "≈ 30 minutes",
        "format": "4 sections · 40 questions",
        "intro": (
            "The Listening test has four sections and 40 questions in total. "
            "You will hear the recording once only, so listen carefully and "
            "answer as you go."
        ),
        "instructions": [
            "Put on your headphones and find a quiet place.",
            "The audio plays once from start to finish — you cannot pause or rewind.",
            "Answer each question while you listen.",
            "Spelling matters in gap-fill answers.",
        ],
        "notes": [
            "Press play only when you are ready — the recording does not stop.",
            "All four sections play in one continuous track.",
        ],
        "start_url": ("practice_test:listening", {}),
    },
    "reading": {
        "name": "Academic Reading",
        "accent": "orange",
        "duration": "60 minutes",
        "format": "3 passages · 40 questions",
        "intro": (
            "The Academic Reading test has three passages with a total of 40 "
            "questions. You have 60 minutes to read the passages and answer "
            "every question."
        ),
        "instructions": [
            "Read each passage carefully, then answer the questions that follow.",
            "Answer all 40 questions — there is no penalty for guessing.",
            "Write answers exactly; spelling and grammar are marked.",
            "You can move freely between passages and questions.",
        ],
        "notes": [
            "The 60-minute timer starts as soon as you begin.",
            "There is no extra time to transfer answers.",
        ],
        "start_url": ("reading:academic_test_session", {"test_number": 1}),
    },
    "writing": {
        "name": "Academic Writing",
        "accent": "purple",
        "duration": "60 minutes",
        "format": "Task 1 + Task 2",
        "intro": (
            "The Academic Writing test has two tasks. Spend about 20 minutes on "
            "Task 1 and 40 minutes on Task 2. Your responses are assessed by AI "
            "for a band score."
        ),
        "instructions": [
            "Task 1: describe the visual information in at least 150 words.",
            "Task 2: write an essay answering the prompt in at least 250 words.",
            "Task 2 carries more marks than Task 1 — plan your time.",
            "Write in full, formal English.",
        ],
        "notes": [
            "You will receive an AI band score with feedback after you submit.",
            "Spend roughly 20 min on Task 1 and 40 min on Task 2.",
        ],
        "start_url": ("practice_test:writing", {}),
    },
    "speaking": {
        "name": "Speaking",
        "accent": "green",
        "duration": "≈ 11–15 minutes",
        "format": "3 parts · recorded",
        "intro": (
            "The Speaking test has three parts led by a video examiner. Your "
            "answers are recorded and assessed by AI for fluency, vocabulary, "
            "grammar and pronunciation."
        ),
        "instructions": [
            "Part 1: short questions about familiar topics.",
            "Part 2: speak for 1–2 minutes on a cue-card topic.",
            "Part 3: a discussion of more abstract questions.",
            "Speak naturally and clearly into your microphone.",
        ],
        "notes": [
            "You will check your headphones and microphone before starting.",
            "Recording begins automatically after each examiner question.",
        ],
        "start_url": ("practice_test:speaking", {}),
    },
}


@login_required
def exam_intro(request, section):
    """Professional IELTS-style instructions screen with a 'Start exam' button."""
    cfg = EXAM_INTROS.get(section)
    if cfg is None:
        return redirect("reading:academic_tests_index")
    url_name, kwargs = cfg["start_url"]
    return render(
        request,
        "practice_test/exam_intro.html",
        {
            "section": section,
            "cfg": cfg,
            "start_url": reverse(url_name, kwargs=kwargs),
        },
    )


@login_required
def listening(request):
    n = _active_test(request)
    ldict = _listening_dict_for(n)
    sections_raw = ldict.get("sections", [])
    total = sum(len(s["questions"]) for s in sections_raw)

    # Test 1 uses one stitched track generated by tts; Tests 2–5 use four
    # separate per-section audio files served from static/.
    if n == 1:
        if not tts.audio_exists():
            return render(
                request,
                "practice_test/listening_setup.html",
                {
                    "section_count": len(sections_raw),
                    "question_count": total,
                },
            )
        return render(
            request,
            "practice_test/listening.html",
            {
                "sections": _listening_sections_with_numbers(sections_raw),
                "total": total,
                "minutes": ldict.get("minutes", 30),
                "review_seconds": 120,
                "audio_url": tts.audio_url(),
                "audio_timing": tts.audio_timing(),
                "section_audios": [],
                "test_number": n,
            },
        )

    from django.templatetags.static import static as _static
    section_audios = [
        {"number": s["number"], "url": _static(f"listening_audio/{s['audio']}")}
        for s in sections_raw if s.get("audio")
    ]
    return render(
        request,
        "practice_test/listening.html",
        {
            "sections": _listening_sections_with_numbers(sections_raw),
            "total": total,
            "minutes": ldict.get("minutes", 30),
            "review_seconds": 120,
            "audio_url": "",
            "audio_timing": [],
            "section_audios": section_audios,
            "test_number": n,
        },
    )


@login_required
@require_POST
def listening_prepare(request):
    """Generate the listening audio synchronously (~30–60s)."""
    if tts.audio_exists():
        return redirect("practice_test:listening")
    try:
        tts.generate_audio(verbose=False)
    except Exception as exc:
        return render(
            request,
            "practice_test/listening_setup.html",
            {
                "section_count": len(LC.LISTENING_TEST["sections"]),
                "question_count": LC.total_questions(),
                "error": str(exc),
            },
            status=500,
        )
    return redirect("practice_test:listening")


@login_required
@require_POST
def listening_submit(request):
    n = _active_test(request)
    g = _grade_listening(request.POST, _listening_dict_for(n).get("sections", []))
    session = TestSession.objects.create(
        user=request.user,
        kind=TestSession.KIND_LISTENING,
        status=TestSession.STATUS_COMPLETED,
        band_overall=g["band"],
        band_listening=g["band"],
        completed_at=timezone.now(),
        raw={
            "answers":    g["answers"],
            "correct":    g["correct"],
            "total":      g["total"],
            "by_section": g["by_section"],
        },
    )
    return redirect("practice_test:results", session_id=session.id)


@login_required
def reading(request):
    n = _active_test(request)
    passages = _reading_passages_for(n)
    return render(
        request,
        "practice_test/reading.html",
        {
            "passages": _annotated_passages(passages),
            "total": sum(len(p["questions"]) for p in passages),
            "minutes": 60,
            "test_number": n,
        },
    )


@login_required
@require_POST
def reading_submit(request):
    n = _active_test(request)
    g = _grade_reading(request.POST, _reading_passages_for(n))
    session = TestSession.objects.create(
        user=request.user,
        kind=TestSession.KIND_READING,
        status=TestSession.STATUS_COMPLETED,
        band_overall=g["band"],
        band_reading=g["band"],
        completed_at=timezone.now(),
        raw={
            "answers":    g["answers"],
            "correct":    g["correct"],
            "total":      g["total"],
            "by_passage": g["by_passage"],
        },
    )
    return redirect("practice_test:results", session_id=session.id)


@login_required
def writing(request):
    n = _active_test(request)
    tasks = _writing_tasks_for(n)
    return render(
        request,
        "practice_test/writing.html",
        {
            "task1": tasks["task1"],
            "task2": tasks["task2"],
            "test_number": n,
        },
    )


@login_required
@require_POST
def writing_submit(request):
    n = _active_test(request)
    g = _grade_writing(request.POST, _writing_tasks_for(n))
    session = TestSession.objects.create(
        user=request.user,
        kind=TestSession.KIND_WRITING,
        status=TestSession.STATUS_COMPLETED,
        band_overall=g["band"],
        band_writing=g["band"],
        completed_at=timezone.now(),
        raw={"task1": g["task1"], "task2": g["task2"]},
    )
    return redirect("practice_test:results", session_id=session.id)


@login_required
def speaking(request):
    """Standalone /test/speaking/ page — video-driven examiner flow.

    Renders a single self-contained page that handles:
      1) the setup checks (headphones + microphone),
      2) the test stage that plays the SPEAKING_VIDEO_FLOW videos in order,
         records the student's answer after each question and shows AI
         feedback inline, then
      3) on the outro video, finalises the session and redirects to results.

    The full-test ``/test/full/speaking/`` page is a separate template and
    is intentionally untouched.

    Each flow step's ``url`` is resolved through Django's static() helper so
    it works under both StaticFilesStorage (local dev) and the production
    ManifestStaticFilesStorage (filename hashing on Railway).
    """
    from django.templatetags.static import static

    # The examiner-video flow, recording, transcription and scoring are shared
    # across all tests — only the folder (and, for some tests, the filename
    # scheme) the videos load from differs per test.
    n = _active_test(request)
    folder = SPEAKING_VIDEO_FOLDERS.get(n, "speaking_videos")

    session = TestSession.objects.create(
        user=request.user,
        kind=TestSession.KIND_SPEAKING,
    )
    flow_with_urls = [
        {**step, "url": static(f"{folder}/" + _speaking_video_file(n, step["video"]))}
        for step in C.SPEAKING_VIDEO_FLOW
    ]
    return render(
        request,
        "practice_test/speaking.html",
        {
            "session": session,
            "flow": flow_with_urls,
            "sample_video_url": static(f"{folder}/" + _speaking_video_file(n, "intro.mp4")),
            "total_questions": C.speaking_video_questions_total(),
        },
    )


@login_required
@csrf_protect
@require_POST
def speaking_submit_answer(request):
    """POST /test/speaking/submit-answer/ for the video-driven speaking page.

    During the test we ONLY persist the recorded audio and return instantly.
    Transcription (Whisper) and the AI report are intentionally NOT run here:
    doing them per question made the "Saving answer…" step block for many
    seconds each time. All of that heavy work now happens once, in parallel,
    in ``speaking_finish`` after the outro video.
    """
    sid = request.POST.get("session_id")
    if not sid:
        return JsonResponse({"ok": False, "error": "missing session_id"}, status=400)
    session = get_object_or_404(
        TestSession, id=sid, user=request.user, kind=TestSession.KIND_SPEAKING,
    )

    try:
        part = int(request.POST.get("part") or 0)
        qi   = int(request.POST.get("question_index") or 0)
    except ValueError:
        return JsonResponse({"ok": False, "error": "bad indices"}, status=400)
    if part not in (1, 2, 3):
        return JsonResponse({"ok": False, "error": "bad part"}, status=400)

    question_text = (request.POST.get("question_text") or "").strip()
    audio = request.FILES.get("audio")
    if audio is None:
        return JsonResponse({"ok": False, "error": "missing audio"}, status=400)

    try:
        duration = float(request.POST.get("duration_seconds") or 0)
    except ValueError:
        duration = 0.0

    # Replace any earlier attempt at this exact (part, question_index) — the
    # video flow lets the student re-record a question before moving on.
    SpeakingResponse.objects.filter(
        session=session, part=part, question_index=qi,
    ).delete()

    resp = SpeakingResponse.objects.create(
        session=session,
        user=request.user,
        part=part,
        question_index=qi,
        question_text=question_text,
        audio=audio,
        duration_seconds=duration,
    )

    return JsonResponse({"ok": True, "response_id": resp.id})


def _transcribe_session_responses(responses: list) -> None:
    """Transcribe every answer that doesn't yet have a transcript, in parallel.

    Whisper calls are network/IO bound, so a small thread pool lets us process
    all ~11 answers in a few waves instead of one-at-a-time. The worker only
    touches the file system + OpenAI (no DB), and the main thread writes the
    results back — so there are no cross-thread database-connection issues.
    """
    import os as _os
    from concurrent.futures import ThreadPoolExecutor

    todo = [r for r in responses if not (r.transcript or "").strip()]
    if not todo:
        return

    def _work(resp):
        path = resp.audio.path if resp.audio else None
        if not path or not _os.path.exists(path):
            return resp.id, "", "No audio file was saved on the server.", {}
        transcript, err, meta = transcribe_audio(path)
        return resp.id, transcript, err, meta

    by_id = {r.id: r for r in todo}
    with ThreadPoolExecutor(max_workers=min(6, len(todo))) as pool:
        results = list(pool.map(_work, todo))

    for rid, transcript, transcribe_error, whisper_meta in results:
        resp = by_id.get(rid)
        if resp is None:
            continue
        resp.transcript = transcript
        resp.raw = {
            **(resp.raw or {}),
            "transcribe_error": transcribe_error,
            "whisper": {
                "duration": whisper_meta.get("duration"),
                "language": whisper_meta.get("language"),
            },
        }
        resp.save(update_fields=["transcript", "raw"])


def _build_speaking_report(session) -> dict:
    """Generate the consolidated speaking report and cache it on the session.

    Transcribes any answers that still need it (in parallel), then runs the
    single report-synthesis GPT call. The result is stored on
    ``session.raw["report"]`` so subsequent loads of the results page don't
    re-call OpenAI. The cached copy is the source of truth for the new
    speaking_results template.
    """
    responses = list(
        SpeakingResponse.objects.filter(session=session)
        .order_by("part", "question_index")
    )
    _transcribe_session_responses(responses)
    report = synthesize_speaking_report(responses)
    session.raw = session.raw or {}
    session.raw["report"] = report
    if report.get("overall_band"):
        session.band_overall = report["overall_band"]
        session.band_speaking = report["overall_band"]
    session.save(update_fields=["raw", "band_overall", "band_speaking"])
    return report


@login_required
@csrf_protect
@require_POST
def speaking_finish(request):
    """POST endpoint hit when the outro video ends — finalises the session,
    generates the consolidated AI report and returns the URL to redirect to.
    """
    sid = request.POST.get("session_id")
    if not sid:
        return JsonResponse({"ok": False, "error": "missing session_id"}, status=400)
    session = get_object_or_404(
        TestSession, id=sid, user=request.user, kind=TestSession.KIND_SPEAKING,
    )
    # Mark the session complete, then transcribe every answer in parallel and
    # run the single report-synthesis call. The report's band is the real
    # overall score (per-question scoring no longer runs during the test).
    _finalise_speaking_session(session)
    report = _build_speaking_report(session)
    return JsonResponse({
        "ok": True,
        "overall": report.get("overall_band"),
        "results_url": reverse("practice_test:speaking_results", args=[session.id]),
    })


@login_required
def speaking_results(request, session_id: int):
    """Dedicated /test/speaking/results/<id>/ page.

    Renders only the five sections required by the speaking results spec:
    score header, full transcript, errors & corrections, better answer
    examples, improvement tips. The general ``/test/results/<id>/`` page
    used by reading / writing / listening is intentionally left alone.
    """
    session = get_object_or_404(
        TestSession, id=session_id, user=request.user, kind=TestSession.KIND_SPEAKING,
    )
    report = (session.raw or {}).get("report")
    # First visit (or older sessions created before the report cache existed)
    # — generate it lazily so the page still works.
    if not isinstance(report, dict) or not report.get("transcript"):
        report = _build_speaking_report(session)
    return render(
        request,
        "practice_test/speaking_results.html",
        {
            "session": session,
            "report":  report,
        },
    )


@login_required
@csrf_protect
@require_http_methods(["POST"])
def speaking_score_api(request):
    """Multipart upload: audio + part + question_index → transcribe + score.

    Shared by both standalone and full-test speaking pages — the API doesn't
    care which page the audio came from, it just scores one answer.
    """
    sid = request.POST.get("session_id")
    try:
        part = int(request.POST.get("part") or 0)
        qi = int(request.POST.get("question_index") or 0)
    except ValueError:
        return JsonResponse({"ok": False, "error": "bad indices"}, status=400)

    if part not in (1, 2, 3):
        return JsonResponse({"ok": False, "error": "bad part"}, status=400)

    questions = next((p["questions"] for p in C.SPEAKING_PARTS if p["part"] == part), [])
    if qi < 0 or qi >= len(questions):
        return JsonResponse({"ok": False, "error": "bad question_index"}, status=400)

    audio = request.FILES.get("audio")
    if audio is None:
        return JsonResponse({"ok": False, "error": "missing audio"}, status=400)

    try:
        duration = float(request.POST.get("duration_seconds") or 0)
    except ValueError:
        duration = 0.0

    session = (
        get_object_or_404(TestSession, id=sid, user=request.user)
        if sid
        else _get_or_create_speaking_session(request.user)
    )

    question_text = questions[qi]
    resp = SpeakingResponse.objects.create(
        session=session,
        user=request.user,
        part=part,
        question_index=qi,
        question_text=question_text,
        audio=audio,
        duration_seconds=duration,
    )
    if resp.audio:
        transcript, transcribe_error, whisper_meta = transcribe_audio(resp.audio.path)
    else:
        transcript, transcribe_error, whisper_meta = "", "No audio file was saved on the server.", {}
    resp.transcript = transcript

    metrics = _compute_speaking_metrics(transcript, whisper_meta, duration)
    scores = score_speaking(
        part, question_text, transcript, duration, transcribe_error, metrics=metrics
    )
    annotated_html = annotate_speaking_transcript(transcript, scores.get("annotations") or [])
    scores["annotated_html"] = annotated_html

    resp.fluency       = scores.get("fluency")
    resp.vocabulary    = scores.get("vocabulary")
    resp.grammar       = scores.get("grammar")
    resp.pronunciation = scores.get("pronunciation")
    resp.band          = scores.get("band")
    resp.feedback      = scores.get("feedback") or ""
    # Persist everything we just computed — the live UI and results page both
    # render from this dict, and we don't want to call the AI again.
    resp.raw = {
        **scores,
        "transcribe_error": transcribe_error,
        # We deliberately don't store the entire raw Whisper payload (it's huge);
        # only keep the bits we need for "every sound" inspection.
        "whisper": {
            "duration": whisper_meta.get("duration"),
            "language": whisper_meta.get("language"),
        },
    }
    resp.save()

    return JsonResponse({
        "ok": True,
        "transcript": transcript,
        "annotated_html": annotated_html,
        "transcribe_error": transcribe_error,
        "fluency": resp.fluency,
        "vocabulary": resp.vocabulary,
        "grammar": resp.grammar,
        "pronunciation": resp.pronunciation,
        "band": resp.band,
        "feedback": resp.feedback,
        "criteria": scores.get("criteria") or {},
        "annotations": scores.get("annotations") or [],
        "metrics": metrics,
        "session_id": session.id,
        "response_id": resp.id,
    })


@login_required
@csrf_protect
@require_POST
def speaking_rescore_api(request, response_id: int):
    """Re-run transcription + scoring on a previously-saved answer.

    Used by the "Retry" button on the results page after a transient
    ``APIConnectionError`` so the student doesn't have to re-record. The
    user can only rescore their own responses, and only when the audio
    file is still on disk.
    """
    import os

    resp = get_object_or_404(SpeakingResponse, id=response_id, user=request.user)

    if not (resp.audio and os.path.exists(resp.audio.path)):
        return JsonResponse({
            "ok": False,
            "error": "Original recording is no longer available on the server.",
        }, status=400)

    transcript, transcribe_error, whisper_meta = transcribe_audio(resp.audio.path)
    metrics = _compute_speaking_metrics(transcript, whisper_meta, resp.duration_seconds or 0)
    scores = score_speaking(
        resp.part, resp.question_text, transcript,
        resp.duration_seconds or 0, transcribe_error, metrics=metrics,
    )
    annotated_html = annotate_speaking_transcript(transcript, scores.get("annotations") or [])
    scores["annotated_html"] = annotated_html

    resp.transcript    = transcript
    resp.fluency       = scores.get("fluency")
    resp.vocabulary    = scores.get("vocabulary")
    resp.grammar       = scores.get("grammar")
    resp.pronunciation = scores.get("pronunciation")
    resp.band          = scores.get("band")
    resp.feedback      = scores.get("feedback") or ""
    resp.raw = {
        **scores,
        "transcribe_error": transcribe_error,
        "whisper": {
            "duration": whisper_meta.get("duration"),
            "language": whisper_meta.get("language"),
        },
    }
    resp.save()

    # If this response belongs to a completed speaking session, re-aggregate
    # the session-level bands so the headline number on the results page
    # updates too. We deliberately keep the session in its current status
    # (COMPLETED stays COMPLETED) — _finalise_speaking_session is idempotent.
    session = resp.session
    overall = None
    if session and session.kind == TestSession.KIND_SPEAKING:
        overall = _finalise_speaking_session(session)

    return JsonResponse({
        "ok": True,
        "transcript": transcript,
        "annotated_html": annotated_html,
        "transcribe_error": transcribe_error,
        "fluency":       resp.fluency,
        "vocabulary":    resp.vocabulary,
        "grammar":       resp.grammar,
        "pronunciation": resp.pronunciation,
        "band":          resp.band,
        "feedback":      resp.feedback,
        "criteria":      scores.get("criteria") or {},
        "annotations":   scores.get("annotations") or [],
        "metrics":       metrics,
        "session_band":  overall,
        "response_id":   resp.id,
    })


# =============================================================================
# Full Academic Test — completely separate routes + templates
# =============================================================================

FULL_ORDER = ["reading", "writing", "listening", "speaking"]


def _get_full(request) -> TestSession | None:
    """Look up the in-progress Full session passed via `?full=N` or POST `full=N`."""
    fid = request.GET.get("full") or request.POST.get("full")
    if not fid:
        return None
    try:
        return TestSession.objects.get(
            id=int(fid),
            user=request.user,
            kind=TestSession.KIND_FULL,
        )
    except (TestSession.DoesNotExist, ValueError):
        return None


def _full_next_url(full: TestSession, current: str) -> str:
    """URL of the next step (or results if we're past the end)."""
    try:
        idx = FULL_ORDER.index(current)
    except ValueError:
        return reverse("practice_test:results", args=[full.id])
    nxt = FULL_ORDER[idx + 1] if idx + 1 < len(FULL_ORDER) else None
    if nxt is None:
        return reverse("practice_test:results", args=[full.id])
    base = {
        "reading":   reverse("practice_test:full_reading"),
        "writing":   reverse("practice_test:full_writing"),
        "speaking":  reverse("practice_test:full_speaking"),
        "listening": reverse("practice_test:full_listening"),
    }[nxt]
    return f"{base}?full={full.id}"


def _recompute_full_overall(full: TestSession) -> None:
    parts = [full.band_reading, full.band_writing, full.band_speaking, full.band_listening]
    vals = [p for p in parts if isinstance(p, (int, float)) and p > 0]
    full.band_overall = round_half(sum(vals) / len(vals)) if vals else None


def _save_band_to_full(full: TestSession, kind: str, band: float, detail: dict | None = None) -> None:
    setattr(full, f"band_{kind}", band)
    full.raw = full.raw or {}
    if detail is not None:
        full.raw[kind] = detail
    _recompute_full_overall(full)
    full.save()


def _advance_full(full: TestSession, current: str) -> str:
    """Move to the next step — finalise the session if `current` is last."""
    try:
        idx = FULL_ORDER.index(current)
    except ValueError:
        idx = -1
    if idx < 0 or idx + 1 >= len(FULL_ORDER):
        _recompute_full_overall(full)
        full.status = TestSession.STATUS_COMPLETED
        full.completed_at = timezone.now()
        full.save()
        return reverse("practice_test:results", args=[full.id])
    return _full_next_url(full, current)


def _step_ctx(full: TestSession, current: str) -> dict:
    """Step-bar context for the full-test runner pages."""
    steps = []
    for i, name in enumerate(FULL_ORDER, start=1):
        band = getattr(full, f"band_{name}")
        idx_cur = FULL_ORDER.index(current) if current in FULL_ORDER else -1
        steps.append({
            "name": name,
            "label": name.title(),
            "number": i,
            "band": band,
            "done": band is not None,
            "current": (i - 1) == idx_cur,
            "future": (i - 1) > idx_cur,
        })
    return {"full_id": full.id, "steps": steps, "full_session": full}


# ----- Full intro -----

@login_required
def full_test(request):
    session = (
        TestSession.objects.filter(
            user=request.user,
            kind=TestSession.KIND_FULL,
            status=TestSession.STATUS_IN_PROGRESS,
        )
        .order_by("-started_at")
        .first()
    )
    if session is None:
        session = TestSession.objects.create(user=request.user, kind=TestSession.KIND_FULL)
    return render(
        request,
        "practice_test/full.html",
        {
            "session": session,
            "listening_available": C.LISTENING_AVAILABLE,
            **_step_ctx(session, ""),
        },
    )


# ----- Full · Reading -----

@login_required
def full_reading(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")
    return render(
        request,
        "practice_test/full_reading.html",
        {
            "passages": _annotated_passages(),
            "total": C.reading_total_questions(),
            "minutes": 60,
            **_step_ctx(full, "reading"),
        },
    )


@login_required
@require_POST
def full_reading_submit(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")
    g = _grade_reading(request.POST)
    _save_band_to_full(full, "reading", g["band"], {
        "correct":    g["correct"],
        "total":      g["total"],
        "by_passage": g["by_passage"],
    })
    return redirect(_advance_full(full, "reading"))


# ----- Full · Writing -----

@login_required
def full_writing(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")
    return render(
        request,
        "practice_test/full_writing.html",
        {
            "task1": C.WRITING_TASKS["task1"],
            "task2": C.WRITING_TASKS["task2"],
            **_step_ctx(full, "writing"),
        },
    )


@login_required
@require_POST
def full_writing_submit(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")
    g = _grade_writing(request.POST)
    _save_band_to_full(full, "writing", g["band"], {
        "task1": {"word_count": g["task1"]["word_count"], "band": g["task1"]["band"]},
        "task2": {"word_count": g["task2"]["word_count"], "band": g["task2"]["band"]},
        "summary_task1": g["task1"]["feedback"].get("summary", ""),
        "summary_task2": g["task2"]["feedback"].get("summary", ""),
    })
    return redirect(_advance_full(full, "writing"))


# ----- Full · Listening -----

@login_required
def full_listening(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")

    # Audio not yet generated → show the same setup screen but inside the full-test shell.
    if not tts.audio_exists():
        return render(
            request,
            "practice_test/full_listening_setup.html",
            {
                "section_count": len(LC.LISTENING_TEST["sections"]),
                "question_count": LC.total_questions(),
                **_step_ctx(full, "listening"),
            },
        )

    return render(
        request,
        "practice_test/full_listening.html",
        {
            "sections": _listening_sections_with_numbers(),
            "total": LC.total_questions(),
            "minutes": 30,
            "audio_url": tts.audio_url(),
            **_step_ctx(full, "listening"),
        },
    )


@login_required
@require_POST
def full_listening_submit(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")
    g = _grade_listening(request.POST)
    _save_band_to_full(full, "listening", g["band"], {
        "correct":    g["correct"],
        "total":      g["total"],
        "by_section": g["by_section"],
    })
    return redirect(_advance_full(full, "listening"))


# ----- Full · Speaking -----

@login_required
def full_speaking(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:full")

    if request.method == "POST" and request.POST.get("action") == "finish":
        sid = request.POST.get("session_id")
        if not sid:
            return HttpResponseBadRequest("missing session_id")
        spk = get_object_or_404(TestSession, id=sid, user=request.user)
        band = _finalise_speaking_session(spk)
        if not SpeakingResponse.objects.filter(session=spk).exists():
            return redirect(f"{reverse('practice_test:full_speaking')}?full={full.id}")
        _save_band_to_full(full, "speaking", band, {
            "fluency": spk.raw.get("fluency"),
            "vocabulary": spk.raw.get("vocabulary"),
            "grammar": spk.raw.get("grammar"),
            "pronunciation": spk.raw.get("pronunciation"),
            "answered": spk.raw.get("answered"),
        })
        return redirect(_advance_full(full, "speaking"))

    spk = _get_or_create_speaking_session(request.user)
    responses = list(SpeakingResponse.objects.filter(session=spk).order_by("part", "question_index"))
    answered = {(r.part, r.question_index): r for r in responses}
    return render(
        request,
        "practice_test/full_speaking.html",
        {
            "session": spk,
            "parts": C.SPEAKING_PARTS,
            "answered": answered,
            "total_questions": C.speaking_total_questions(),
            "answered_count": len(responses),
            **_step_ctx(full, "speaking"),
        },
    )


# ----- Full · Manual finish (e.g. from the Listening Coming soon screen if a
# student decides to stop early) -----

@login_required
@require_POST
def full_finish(request):
    full = _get_full(request)
    if full is None:
        return redirect("practice_test:hub")
    _recompute_full_overall(full)
    full.status = TestSession.STATUS_COMPLETED
    full.completed_at = timezone.now()
    full.save()
    return redirect("practice_test:results", session_id=full.id)


# =============================================================================
# Results
# =============================================================================

@login_required
def results(request, session_id: int):
    session = get_object_or_404(TestSession, id=session_id, user=request.user)
    speaking_responses = (
        list(SpeakingResponse.objects.filter(session=session).order_by("part", "question_index"))
        if session.kind == TestSession.KIND_SPEAKING
        else []
    )
    # Count answers whose transcription failed but still have audio on disk —
    # those are the ones the Retry button can recover without re-recording.
    speaking_failed_count = sum(
        1 for r in speaking_responses
        if (not (r.transcript or "").strip()) and r.audio
    )
    return render(
        request,
        "practice_test/results.html",
        {
            "session": session,
            "speaking_responses": speaking_responses,
            "speaking_failed_count": speaking_failed_count,
        },
    )
