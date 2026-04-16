from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .coaching import (
    coach_round_one,
    coach_round_three,
    coach_round_two,
    count_sentences,
    generate_paraphrase_source,
    paraphrase_feedback,
)
from .forms import CoachingDraftForm, ParaphraseForm
from .grading import essay_word_count, grade_task1_response, grade_task2_essay, parse_vocabulary_lines
from .models import Essay, ParaphrasePractice, WordBankEntry, WritingCoachingSession, WritingQuestion


def _parse_level(raw: str | None) -> int:
    try:
        v = int((raw or "3").strip())
        return v if v in (1, 2, 3) else 3
    except ValueError:
        return 3


def _parse_qtype(raw: str | None) -> str:
    v = (raw or WritingQuestion.TASK2).strip().lower()
    return WritingQuestion.TASK1 if v == "task1" else WritingQuestion.TASK2


TASK1_KINDS = frozenset(
    {
        WritingQuestion.T1_CHART,
        WritingQuestion.T1_TABLE,
        WritingQuestion.T1_PROCESS,
        WritingQuestion.T1_MAP,
    }
)
TASK2_KINDS = frozenset(
    {
        WritingQuestion.T2_OPINION,
        WritingQuestion.T2_DISCUSSION,
        WritingQuestion.T2_PROBLEM,
        WritingQuestion.T2_ADVANTAGES,
        WritingQuestion.T2_TWO_PART,
    }
)


def _normalize_prompt_kind(qtype: str, raw: str | None) -> str:
    k = (raw or "").strip()
    if not k:
        return ""
    allowed = TASK1_KINDS if qtype == WritingQuestion.TASK1 else TASK2_KINDS
    return k if k in allowed else ""


def _pick_writing_question(qtype: str, level: int, kind: str):
    qs = WritingQuestion.objects.filter(question_type=qtype, level=level)
    if kind:
        sub = qs.filter(prompt_kind=kind)
        if sub.exists():
            return sub.order_by("?").first()
    return qs.order_by("?").first()


PARAPHRASE_SESSION_KEY = "writing_paraphrase_ctx"


def _target_words(qtype: str, _level: int) -> int:
    """Official IELTS minimums; level only affects feedback tone elsewhere."""
    if qtype == WritingQuestion.TASK1:
        return 150
    return 250


def _timer_seconds(qtype: str, _level: int) -> int:
    if qtype == WritingQuestion.TASK1:
        return 20 * 60
    return 40 * 60


def _min_words_warn(qtype: str, _level: int) -> int:
    if qtype == WritingQuestion.TASK1:
        return 150
    return 250


def _essay_draft_count(e: Essay) -> int:
    n = 1
    try:
        if (e.draft_1 or "").strip():
            n += 1
        if (e.draft_2 or "").strip():
            n += 1
    except Exception:
        return 1
    return n


def _grading_summary(grades: dict) -> str:
    lines = []
    bs = grades.get("band_score")
    if bs is not None:
        lines.append(f"Overall band: {bs}")
    pairs = [
        ("task_achievement_score", "Task achievement"),
        ("coherence_score", "Coherence and cohesion"),
        ("lexical_score", "Lexical resource"),
        ("grammar_score", "Grammar"),
    ]
    for key, label in pairs:
        v = grades.get(key)
        if v is not None:
            lines.append(f"{label}: {v} / 9")
    fb = (grades.get("ai_feedback") or "").strip()
    if fb:
        lines.append("Examiner-style feedback (excerpt):\n" + fb[:1200])
    return "\n".join(lines) if lines else "No numeric scores returned."


@login_required
def writing_task1_redirect(request: HttpRequest) -> HttpResponse:
    return redirect(f"{reverse('writing:pick')}?qtype=task1")


@login_required
def writing_task2_redirect(request: HttpRequest) -> HttpResponse:
    return redirect(f"{reverse('writing:pick')}?qtype=task2")


@login_required
def writing_home(request: HttpRequest) -> HttpResponse:
    user = request.user
    latest_band = None
    essays_count = 0
    streak = 0
    writing_history: list[dict] = []

    try:
        essays_count = Essay.objects.filter(student=user).count()
    except Exception:
        essays_count = 0

    try:
        latest = Essay.objects.filter(student=user).order_by("-submitted_at").first()
        if latest is not None and latest.band_score is not None:
            latest_band = latest.band_score
    except Exception:
        latest_band = None

    try:
        streak = int(getattr(getattr(user, "profile", None), "streak", 0) or 0)
    except Exception:
        streak = 0

    try:
        for e in Essay.objects.filter(student=user).order_by("-submitted_at")[:8]:
            task_label = e.get_question_type_display()
            qdetail = ""
            try:
                if e.writing_question_id and e.writing_question is not None:
                    qdetail = e.writing_question.get_prompt_kind_display() or e.writing_question.get_topic_display()
                else:
                    qdetail = (e.question or "")[:80]
            except Exception:
                qdetail = "Essay"
            band_val = e.band_score if e.band_score is not None else "—"
            writing_history.append(
                {
                    "task_type": task_label,
                    "question_type": qdetail,
                    "band_score": band_val,
                    "created_at": e.submitted_at,
                    "drafts": _essay_draft_count(e),
                }
            )
    except Exception:
        writing_history = []

    return render(
        request,
        "writing/writing_home.html",
        {
            "latest_band": latest_band,
            "essays_count": essays_count,
            "writing_history": writing_history,
            "streak": streak,
        },
    )


@login_required
def task_chooser(request: HttpRequest) -> HttpResponse:
    qtype_raw = (
        (request.GET.get("qtype") or request.POST.get("qtype") or "task1").strip().lower()
    )
    qtype = WritingQuestion.TASK1 if qtype_raw == "task1" else WritingQuestion.TASK2

    if request.method == "POST":
        level = _parse_level(request.POST.get("level"))
        kind = _normalize_prompt_kind(qtype, request.POST.get("prompt_kind"))
        base = reverse("writing:question")
        q = f"qtype={qtype}&level={level}"
        if kind:
            q += f"&kind={kind}"
        return redirect(f"{base}?{q}")

    kinds = (
        [
            (WritingQuestion.T1_CHART, "Charts & graphs (bar, line, pie)"),
            (WritingQuestion.T1_TABLE, "Tables"),
            (WritingQuestion.T1_PROCESS, "Process / diagram"),
            (WritingQuestion.T1_MAP, "Maps"),
        ]
        if qtype == WritingQuestion.TASK1
        else [
            (WritingQuestion.T2_OPINION, "Opinion / agree–disagree"),
            (WritingQuestion.T2_DISCUSSION, "Discussion (both views)"),
            (WritingQuestion.T2_PROBLEM, "Problem & solution"),
            (WritingQuestion.T2_ADVANTAGES, "Advantages & disadvantages"),
            (WritingQuestion.T2_TWO_PART, "Two-part / direct questions"),
        ]
    )

    return render(
        request,
        "writing/task_chooser.html",
        {
            "qtype": qtype,
            "task_label": "Task 1 · Academic" if qtype == WritingQuestion.TASK1 else "Task 2",
            "kinds": kinds,
        },
    )


@login_required
def writing_question(request: HttpRequest) -> HttpResponse:
    session_id_raw = request.GET.get("session") or request.POST.get("session_id")
    session_id: int | None = None
    if session_id_raw not in (None, ""):
        try:
            session_id = int(session_id_raw)
        except ValueError:
            session_id = None

    coaching_session: WritingCoachingSession | None = None
    if session_id is not None:
        coaching_session = get_object_or_404(
            WritingCoachingSession,
            pk=session_id,
            student=request.user,
        )
        wq = coaching_session.writing_question
        level = wq.level
        qtype = wq.question_type
        picked = wq
        coach_stage = coaching_session.stage
        kind = _normalize_prompt_kind(qtype, coaching_session.writing_question.prompt_kind)
    else:
        level = _parse_level(request.GET.get("level") if request.method == "GET" else request.POST.get("level"))
        qtype = _parse_qtype(
            request.GET.get("qtype") if request.method == "GET" else request.POST.get("question_type")
        )
        kind_raw = (
            request.GET.get("kind")
            if request.method == "GET"
            else request.POST.get("prompt_kind")
        )
        kind = _normalize_prompt_kind(qtype, kind_raw)
        picked = _pick_writing_question(qtype, level, kind)
        coach_stage = 1

    task_label = "Task 1" if qtype == WritingQuestion.TASK1 else "Task 2"
    target_words = _target_words(qtype, level)
    timer_seconds = _timer_seconds(qtype, level)
    min_words_warn = _min_words_warn(qtype, level)
    min_lens = {1: 40, 2: 60, 3: 80}

    if request.method == "POST":
        step = int(request.POST.get("coach_step") or 1)
        form = CoachingDraftForm(
            request.POST,
            min_answer_len=min_lens.get(step, 40),
        )
        if form.is_valid():
            answer = form.cleaned_data["answer"]
            wc = essay_word_count(answer)
            min_w = _min_words_warn(qtype, level)
            if wc < min_w:
                messages.warning(
                    request,
                    f"This draft is {wc} words. Aim for about {min_w}+ words for this task and level.",
                )

            if step == 1 and coaching_session is None:
                wq = get_object_or_404(
                    WritingQuestion,
                    pk=form.cleaned_data["question_id"],
                    level=form.cleaned_data["level"],
                    question_type=form.cleaned_data["question_type"],
                )
                try:
                    r1 = coach_round_one(
                        question_text=wq.question_text,
                        question_type=wq.question_type,
                        draft_text=answer,
                        word_count=wc,
                        learner_level=level,
                    )
                except RuntimeError as exc:
                    messages.error(request, f"AI coaching failed: {exc}")
                    return redirect(request.path)

                sess = WritingCoachingSession.objects.create(
                    student=request.user,
                    writing_question=wq,
                    draft_1=answer,
                    round_1_feedback=r1,
                    stage=2,
                )
                return redirect(f"{request.path}?session={sess.pk}")

            if step == 2 and coaching_session is not None and coaching_session.stage == 2:
                try:
                    r2 = coach_round_two(
                        question_text=coaching_session.writing_question.question_text,
                        question_type=coaching_session.writing_question.question_type,
                        draft_1=coaching_session.draft_1,
                        draft_2=answer,
                        wc1=essay_word_count(coaching_session.draft_1),
                        wc2=wc,
                        round_1_feedback=coaching_session.round_1_feedback,
                        learner_level=level,
                    )
                except RuntimeError as exc:
                    messages.error(request, f"AI coaching failed: {exc}")
                    return redirect(f"{request.path}?session={coaching_session.pk}")

                coaching_session.draft_2 = answer
                coaching_session.round_2_feedback = r2
                coaching_session.stage = 3
                coaching_session.save(update_fields=["draft_2", "round_2_feedback", "stage", "updated_at"])
                return redirect(f"{request.path}?session={coaching_session.pk}")

            if step == 3 and coaching_session is not None and coaching_session.stage == 3:
                wq = coaching_session.writing_question
                grade_fn = (
                    grade_task1_response
                    if wq.question_type == WritingQuestion.TASK1
                    else grade_task2_essay
                )
                try:
                    grades = grade_fn(
                        question_text=wq.question_text,
                        essay_text=answer,
                        word_count=wc,
                        learner_level=level,
                    )
                except RuntimeError as exc:
                    grades = {
                        "band_score": None,
                        "task_achievement_score": None,
                        "coherence_score": None,
                        "lexical_score": None,
                        "grammar_score": None,
                        "ai_feedback": f"Automatic grading failed: {exc}",
                        "grammar_mistakes": "",
                        "vocabulary_suggestions": "",
                        "issue_spans": [],
                        "strength_spans": [],
                    }
                    messages.warning(
                        request,
                        "Draft 3 was saved but automatic grading failed. Check API key.",
                    )

                gsum = _grading_summary(grades)
                try:
                    r3 = coach_round_three(
                        question_text=wq.question_text,
                        question_type=wq.question_type,
                        draft_1=coaching_session.draft_1,
                        draft_2=coaching_session.draft_2,
                        draft_3=answer,
                        wc1=essay_word_count(coaching_session.draft_1),
                        wc2=essay_word_count(coaching_session.draft_2),
                        wc3=wc,
                        grading_summary=gsum,
                        learner_level=level,
                    )
                except RuntimeError as exc:
                    r3 = {"journey_summary": "", "error": str(exc)}
                    messages.warning(request, "Final coaching summary could not be generated.")

                journey = {
                    "round1": coaching_session.round_1_feedback,
                    "round2": coaching_session.round_2_feedback,
                    "round3": r3,
                }

                with transaction.atomic():
                    essay = Essay.objects.create(
                        student=request.user,
                        writing_question=wq,
                        question=wq.question_text,
                        question_type=wq.question_type,
                        draft_1=coaching_session.draft_1,
                        draft_2=coaching_session.draft_2,
                        coaching_journey=journey,
                        student_answer=answer,
                        word_count=wc,
                        band_score=grades.get("band_score"),
                        task_achievement_score=grades.get("task_achievement_score"),
                        coherence_score=grades.get("coherence_score"),
                        lexical_score=grades.get("lexical_score"),
                        grammar_score=grades.get("grammar_score"),
                        ai_feedback=grades.get("ai_feedback") or "",
                        grammar_mistakes=grades.get("grammar_mistakes") or "",
                        vocabulary_suggestions=grades.get("vocabulary_suggestions") or "",
                        feedback_highlights={
                            "issue_spans": grades.get("issue_spans") or [],
                            "strength_spans": grades.get("strength_spans") or [],
                        },
                    )
                    for phrase in parse_vocabulary_lines(grades.get("vocabulary_suggestions") or ""):
                        WordBankEntry.objects.create(
                            user=request.user,
                            essay=essay,
                            phrase=phrase[:500],
                        )
                    coaching_session.delete()

                messages.success(request, "All three drafts submitted — see your results.")
                return redirect("writing:result", pk=essay.pk)

            messages.error(
                request,
                "That submit did not match the current step. Continue from your open practice or start again from Writing.",
            )
            if coaching_session:
                return redirect(f"{request.path}?session={coaching_session.pk}")
            return redirect("writing:home")

        # Invalid form — fall through to re-render
        if coaching_session is not None:
            picked = coaching_session.writing_question
        else:
            picked = (
                WritingQuestion.objects.filter(
                    pk=int(request.POST.get("question_id") or 0),
                    level=_parse_level(request.POST.get("level")),
                    question_type=_parse_qtype(request.POST.get("question_type")),
                ).first()
            )
    else:
        form = None

    if request.method == "GET":
        if coaching_session:
            form = CoachingDraftForm(
                initial={
                    "coach_step": coaching_session.stage,
                    "session_id": coaching_session.pk,
                    "question_id": picked.pk,
                    "level": level,
                    "question_type": qtype,
                },
                min_answer_len=min_lens.get(coaching_session.stage, 40),
            )
        elif picked:
            form = CoachingDraftForm(
                initial={
                    "coach_step": 1,
                    "question_id": picked.pk,
                    "level": level,
                    "question_type": qtype,
                },
                min_answer_len=min_lens[1],
            )

    style_label = ""
    if picked and picked.prompt_kind:
        style_label = picked.get_prompt_kind_display()

    return render(
        request,
        "writing/question.html",
        {
            "level": level,
            "qtype": qtype,
            "task_label": task_label,
            "target_words": target_words,
            "timer_seconds": timer_seconds,
            "min_words_warn": min_words_warn,
            "question": picked,
            "form": form,
            "coaching_session": coaching_session,
            "coach_stage": coach_stage,
            "prompt_kind": kind,
            "question_style_label": style_label,
            "practice_level_label": {1: "Level 1 (simple feedback · ~A2–B1)", 2: "Level 2 (~B1–B2)", 3: "Level 3 (B2+)"}.get(
                level, ""
            ),
        },
    )


@login_required
def writing_result(request: HttpRequest, pk: int) -> HttpResponse:
    essay = get_object_or_404(Essay, pk=pk, student=request.user)
    wq = essay.writing_question
    level = wq.level if wq else 3
    gm = (essay.grammar_mistakes or "").splitlines()
    vs = (essay.vocabulary_suggestions or "").splitlines()
    mistake_lines = [ln.strip() for ln in gm if ln.strip()]
    vocab_lines = [ln.strip() for ln in vs if ln.strip()]
    style_label = wq.get_prompt_kind_display() if wq and wq.prompt_kind else ""
    level_feedback_hint = {
        1: "This page uses simple English in the written feedback (about A2–B1).",
        2: "Feedback is written in clear B1–B2 English.",
        3: "Feedback may use full IELTS terms and detail.",
    }.get(level, "")
    return render(
        request,
        "writing/result.html",
        {
            "essay": essay,
            "level": level,
            "grammar_lines": mistake_lines,
            "vocab_lines": vocab_lines,
            "question_style_label": style_label,
            "level_feedback_hint": level_feedback_hint,
        },
    )


@login_required
def paraphrase_practice(request: HttpRequest) -> HttpResponse:
    if request.GET.get("reset"):
        request.session.pop(PARAPHRASE_SESSION_KEY, None)
        return redirect("writing:paraphrase")

    para_ctx = request.session.get(PARAPHRASE_SESSION_KEY)
    feedback = None
    paraphrase_highlight_text = ""
    form = ParaphraseForm()

    if request.method == "POST":
        action = (request.POST.get("action") or "check").strip()
        if action == "generate":
            topic = (request.POST.get("topic") or "").strip()
            gen_level = _parse_level(request.POST.get("level"))
            valid_topics = {c[0] for c in WritingQuestion.TOPIC_CHOICES}
            if topic not in valid_topics:
                messages.error(request, "Please choose a topic.")
                return redirect("writing:paraphrase")
            topic_label = dict(WritingQuestion.TOPIC_CHOICES).get(topic, topic)
            try:
                source = generate_paraphrase_source(
                    topic_label=topic_label,
                    topic_code=topic,
                    level=gen_level,
                )
            except RuntimeError as exc:
                messages.error(request, str(exc))
                return redirect("writing:paraphrase")
            request.session[PARAPHRASE_SESSION_KEY] = {
                "topic": topic,
                "level": gen_level,
                "source_text": source,
            }
            request.session.modified = True
            messages.success(request, "Here is your practice text. Paraphrase it in your own words below.")
            return redirect("writing:paraphrase")

        form = ParaphraseForm(request.POST)
        para_ctx = request.session.get(PARAPHRASE_SESSION_KEY)
        if not para_ctx or not para_ctx.get("source_text"):
            messages.error(request, "Generate a practice text first (choose topic and level).")
            return redirect("writing:paraphrase")

        level = int(para_ctx.get("level") or 2)
        topic = para_ctx.get("topic") or ""

        if form.is_valid():
            text = form.cleaned_data["text"]
            wc = essay_word_count(text)
            sc = count_sentences(text)
            ok = True
            if level == 1:
                if sc < 2 or sc > 5:
                    messages.error(
                        request,
                        "Level 1: write between 2 and 5 complete sentences (end with . ! or ?).",
                    )
                    ok = False
            elif level == 2:
                if wc < 50 or wc > 70:
                    messages.error(request, "Level 2: use between 50 and 70 words.")
                    ok = False
            else:
                if wc < 70 or wc > 120:
                    messages.error(request, "Level 3: use between 70 and 120 words.")
                    ok = False

            if ok:
                try:
                    feedback = paraphrase_feedback(
                        level=level,
                        text=text,
                        word_count=wc,
                        sentence_count=sc,
                        source_text=para_ctx["source_text"],
                        learner_level=level,
                    )
                    ParaphrasePractice.objects.create(
                        student=request.user,
                        topic=topic,
                        level=level,
                        source_text=para_ctx["source_text"],
                        input_text=text,
                        feedback=feedback,
                    )
                    messages.success(request, "Here is your AI feedback.")
                    paraphrase_highlight_text = text
                    form = ParaphraseForm(initial={"text": text})
                except RuntimeError as exc:
                    messages.error(request, str(exc))

    level_hints = {
        1: "2–5 complete sentences",
        2: "50–70 words",
        3: "70–120 words",
    }
    gen_level_default = _parse_level(request.GET.get("level"))
    active_level = int(para_ctx.get("level") or gen_level_default) if para_ctx else gen_level_default
    level_caption = {
        1: "Simple feedback (A2–B1 English)",
        2: "Clear feedback (B1–B2)",
        3: "Full detail (B2+)",
    }[active_level]

    return render(
        request,
        "writing/paraphrase.html",
        {
            "form": form,
            "level": active_level,
            "level_hint": level_hints[active_level],
            "feedback": feedback,
            "paraphrase_ctx": para_ctx,
            "topic_choices": WritingQuestion.TOPIC_CHOICES,
            "gen_level_default": gen_level_default,
            "level_caption": level_caption,
            "paraphrase_highlight_text": paraphrase_highlight_text,
        },
    )


@login_required
def word_bank(request: HttpRequest) -> HttpResponse:
    import csv

    from django.http import HttpResponse

    from vocabulary.models import CustomCard

    if (request.GET.get("export") or "").strip().lower() == "csv":
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="boosting-score-word-bank.csv"'
        writer = csv.writer(response)
        writer.writerow(["phrase", "source", "created_at"])
        for e in WordBankEntry.objects.filter(user=request.user).order_by("-created_at"):
            src = "writing_feedback" if e.essay_id else "vocabulary"
            writer.writerow([e.phrase, src, e.created_at.isoformat()])
        for c in CustomCard.objects.filter(student=request.user).order_by("-created_at"):
            writer.writerow([c.word, f"flashcard_{c.topic}", c.created_at.isoformat()])
        return response

    entries = WordBankEntry.objects.filter(user=request.user).order_by("-created_at")
    q = (request.GET.get("q") or "").strip()
    if q:
        entries = entries.filter(phrase__icontains=q)

    flt = (request.GET.get("filter") or "all").strip().lower()
    my_cards = []
    if flt == "vocabulary":
        entries = entries.filter(essay__isnull=True)
    elif flt == "writing":
        entries = entries.filter(essay__isnull=False)
    elif flt == "mycards":
        entries = WordBankEntry.objects.none()
        my_cards = list(
            CustomCard.objects.filter(student=request.user).order_by("-created_at")[:200]
        )

    return render(
        request,
        "writing/word_bank.html",
        {
            "entries": entries,
            "my_cards": my_cards,
            "current_filter": flt,
            "search_q": q,
        },
    )
