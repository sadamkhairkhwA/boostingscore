import json
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse
from openai import OpenAI

from boostingscore.plan_limits import (
    FEATURE_WRITING_GRAMMAR,
    FEATURE_WRITING_LESSONS,
    FEATURE_WRITING_PARAPHRASE,
    FEATURE_WRITING_TASK1,
    FEATURE_WRITING_TASK2,
    ai_limit_json,
    guard_ai_check,
    guard_feature,
    user_can,
)
from vocabulary.streak_utils import bump_streak_for_user

from .lesson_lectures import get_lesson_lecture
from .lesson_practice_data import get_lesson_practice
from .models import (
    Essay,
    GrammarTopicProgress,
    LessonPracticeAttempt,
    LessonProgress,
    SkillProgress,
    WritingTask1Attempt,
    WritingTask2Attempt,
)
from .task1_charts import render_question_chart
from .task1_content import (
    TASK_INSTRUCTION,
    TYPE_META,
    get_question,
    get_questions_by_type,
    question_type_list,
)
from .content import LESSONS, SKILL_MAP, SKILLS, TASK2_QUESTIONS, TASK2_TYPE_META
from .grammar_content import GRAMMAR_TOPICS, get_grammar_topic
from .paraphrase_content import PARAPHRASE_TOPICS, pick_sentence

CRITERION_META = {
    "task_achievement": {
        "label": "Task Achievement",
        "color": "#3b82f6",
        "tag_bg": "#dbeafe",
        "status_good": "Good",
    },
    "coherence_cohesion": {
        "label": "Coherence & Cohesion",
        "color": "#22c55e",
        "tag_bg": "#dcfce7",
        "status_good": "Good",
    },
    "lexical_resource": {
        "label": "Lexical Resource",
        "color": "#f59e0b",
        "tag_bg": "#fef3c7",
        "status_good": "Needs work",
    },
    "grammar_accuracy": {
        "label": "Grammar Range & Accuracy",
        "color": "#f43f5e",
        "tag_bg": "#ffe4e6",
        "status_good": "Good",
    },
}


def _streak_ctx(request):
    streak = getattr(getattr(request.user, "profile", None), "streak", 0) or 0
    return {"streak": streak}


def _word_count(text):
    return len([w for w in (text or "").split() if w.strip()])


def _extract_json(text):
    text = (text or "").strip()
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return {}
    try:
        return json.loads(m.group())
    except json.JSONDecodeError:
        return {}


def _essay_feedback(task_label, question, essay_text):
    if not settings.OPENAI_API_KEY:
        return {
            "band": 6.0,
            "summary": "OpenAI API key is not configured. This is placeholder feedback.",
            "criteria": {},
        }
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (
        f"You are an IELTS writing examiner. Evaluate this {task_label} response.\n\n"
        f"Question:\n{question}\n\nStudent essay:\n{essay_text}\n\n"
        "Return ONLY valid JSON with keys: band (float 0-9), summary (string), "
        "criteria (object with task_response, coherence, lexical, grammar each having "
        "short_comment and score 0-9), improvements (array of strings)."
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
        temperature=0.25,
        messages=[
            {"role": "system", "content": "You return strict JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    raw = completion.choices[0].message.content or ""
    data = _extract_json(raw)
    if not data:
        data = {
            "band": 6.0,
            "summary": raw[:2000],
            "criteria": {},
            "improvements": [],
        }
    return data


@login_required
def writing_home(request):
    essays = Essay.objects.filter(student=request.user).order_by("-created_at")[:20]
    return render(
        request,
        "writing/writing_home.html",
        {
            "essays": essays,
            **_streak_ctx(request),
        },
    )


@login_required
def task1(request):
    question = (
        "The chart below shows the percentage of households in one country that used selected "
        "forms of transport to travel to work in one year. Summarise the information by selecting "
        "and reporting the main features, and make comparisons where relevant.\n\n"
        "(Imagine an appropriate chart is provided.)"
    )
    feedback = None
    saved = None
    essay_text_value = ""
    if request.method == "POST":
        essay_text_value = request.POST.get("essay_text") or ""
        wc = _word_count(essay_text_value)
        fb = _essay_feedback("Task 1", question, essay_text_value)
        band = float(fb.get("band") or 0)
        saved = Essay.objects.create(
            student=request.user,
            task_type="1",
            question=question,
            essay_text=essay_text_value,
            word_count=wc,
            band_score=band,
            feedback_json=fb,
        )
        bump_streak_for_user(request.user)
        feedback = fb

    return render(
        request,
        "writing/task1.html",
        {
            "question": question,
            "essay_text_value": essay_text_value,
            "feedback": feedback,
            "saved": saved,
            **_streak_ctx(request),
        },
    )


@login_required
def task2(request):
    question = (
        "Some people believe that the best way to reduce crime is to give longer prison sentences. "
        "Others believe there are better alternatives. Discuss both views and give your opinion."
    )
    feedback = None
    saved = None
    essay_text_value = ""
    if request.method == "POST":
        essay_text_value = request.POST.get("essay_text") or ""
        wc = _word_count(essay_text_value)
        fb = _essay_feedback("Task 2", question, essay_text_value)
        band = float(fb.get("band") or 0)
        saved = Essay.objects.create(
            student=request.user,
            task_type="2",
            question=question,
            essay_text=essay_text_value,
            word_count=wc,
            band_score=band,
            feedback_json=fb,
        )
        bump_streak_for_user(request.user)
        feedback = fb

    return render(
        request,
        "writing/task2.html",
        {
            "question": question,
            "essay_text_value": essay_text_value,
            "feedback": feedback,
            "saved": saved,
            **_streak_ctx(request),
        },
    )


@login_required
def paraphrase(request):
    blocked = guard_feature(request, FEATURE_WRITING_PARAPHRASE)
    if blocked:
        return blocked
    initial = pick_sentence(topic="all")
    return render(
        request,
        "writing/paraphrase.html",
        {
            "topics": PARAPHRASE_TOPICS,
            "initial_sentence": initial["sentence"],
            "initial_topic": initial["topic"],
            "initial_topic_label": initial["topic_label"],
            **_streak_ctx(request),
        },
    )


PARAPHRASE_TECHNIQUE_KEYS = (
    "synonym_replacement",
    "word_form_change",
    "voice_change",
    "clause_structure_change",
)


def _normalize_paraphrase_feedback(data: dict) -> dict:
    techniques_raw = data.get("techniques") or {}
    if not isinstance(techniques_raw, dict):
        techniques_raw = {}
    techniques = {
        key: bool(techniques_raw.get(key))
        for key in PARAPHRASE_TECHNIQUE_KEYS
    }

    similarity = str(data.get("similarity") or "medium").strip().lower()
    if similarity not in {"low", "medium", "high"}:
        similarity = "medium"

    models_raw = data.get("model_paraphrases") or []
    if not isinstance(models_raw, list):
        models_raw = []
    model_paraphrases = []
    for item in models_raw[:3]:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        model_paraphrases.append(
            {
                "technique": str(item.get("technique") or "").strip(),
                "label": str(item.get("label") or item.get("technique") or "").strip(),
                "text": text,
            }
        )

    band = _safe_float(data.get("band_score") or data.get("score"), 6.0)
    band = max(1.0, min(9.0, band))
    verdict = str(data.get("verdict") or "").strip()
    if not verdict:
        verdict = f"Band {band:.1f} — reasonable attempt; keep varying structure and vocabulary."

    return {
        "band_score": band,
        "verdict": verdict,
        "techniques": techniques,
        "feedback": str(data.get("feedback") or "").strip(),
        "similarity": similarity,
        "similarity_note": str(data.get("similarity_note") or "").strip(),
        "model_paraphrases": model_paraphrases,
    }


def _paraphrase_eval(source_text: str, paraphrase_text: str) -> dict | None:
    if not settings.OPENAI_API_KEY:
        return _normalize_paraphrase_feedback(
            {
                "band_score": 0,
                "verdict": "Configure OpenAI to receive live feedback.",
                "techniques": {k: False for k in PARAPHRASE_TECHNIQUE_KEYS},
                "feedback": "Add OPENAI_API_KEY for detailed technique-based feedback.",
                "similarity": "medium",
                "similarity_note": "",
                "model_paraphrases": [],
            }
        )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""You are an IELTS Writing coach evaluating a paraphrase exercise.

SOURCE SENTENCE:
{source_text}

STUDENT'S PARAPHRASE:
{paraphrase_text}

Analyse the student's paraphrase carefully. Detect which paraphrasing TECHNIQUES they actually used (be accurate — only mark true if clearly present):
1. synonym_replacement — key content words swapped for different words (not just one word)
2. word_form_change — same idea expressed with a different word class (noun↔verb↔adjective, e.g. "investment" → "invest", "pollution" → "pollute")
3. voice_change — active↔passive transformation (or clear equivalent)
4. clause_structure_change — sentence reorganised (clause order, subordination, splitting/merging, different grammatical frame)

Also judge:
- Overall quality as an IELTS band-style score (1–9)
- How close the wording is to the source: similarity = "low", "medium", or "high" (high = too close / mostly copied — warn them)
- Write feedback as 1–2 sentences: one strength + the single most useful improvement, phrased in terms of the techniques (e.g. "You replaced vocabulary well but kept the same structure — try changing the grammar too")

Provide 2–3 model_paraphrases of the SOURCE sentence (not the student's text). Each must use a DIFFERENT technique from the list above and include a short label naming that technique.

Return ONLY valid JSON with these keys:
- band_score: float 1–9
- verdict: string — one short line combining band + overall judgement (e.g. "Band 6.5 — meaning clear, but wording stays too close to the original")
- techniques: object with boolean keys synonym_replacement, word_form_change, voice_change, clause_structure_change
- feedback: string (1–2 sentences as described)
- similarity: "low" | "medium" | "high"
- similarity_note: string — one sentence on overlap with source; if similarity is high, warn that it is too close for IELTS paraphrasing
- model_paraphrases: array of 2–3 objects, each {{"technique": "snake_case key", "label": "short human label", "text": "model paraphrase of SOURCE"}}"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.25,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return JSON only. Be accurate about which techniques the student used. "
                        "Model paraphrases must be of the SOURCE sentence only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        raw = completion.choices[0].message.content or "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = _extract_json(raw) or {}
        return _normalize_paraphrase_feedback(data)
    except Exception:
        return None


@login_required
def paraphrase_sentence_api(request):
    topic = (request.GET.get("topic") or "all").strip().lower()
    exclude = request.GET.get("exclude") or ""
    valid = {code for code, _ in PARAPHRASE_TOPICS}
    if topic not in valid:
        topic = "all"
    return JsonResponse({"ok": True, **pick_sentence(topic=topic, exclude=exclude)})


@login_required
@require_POST
def paraphrase_check(request):
    blocked = guard_feature(request, FEATURE_WRITING_PARAPHRASE, json_response=True)
    if blocked:
        return blocked
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        body = {}
    source = (body.get("source_text") or "").strip()
    attempt = (body.get("paraphrase_text") or "").strip()
    if not source:
        return JsonResponse(
            {"ok": False, "error": "Enter a source sentence before checking."},
            status=400,
        )
    if _word_count(attempt) < 3:
        return JsonResponse(
            {"ok": False, "error": "Write your paraphrase before checking."},
            status=400,
        )
    if settings.OPENAI_API_KEY:
        if guard_ai_check(request.user, "paraphrase", will_call_openai=True):
            return ai_limit_json()
    feedback = _paraphrase_eval(source, attempt)
    if feedback is None:
        return JsonResponse(
            {"ok": False, "error": "Couldn't check your answer. Try again."},
            status=502,
        )
    bump_streak_for_user(request.user)
    return JsonResponse({"ok": True, "feedback": feedback})


def _task1_topbar_ctx():
    return {
        "task1_topbar_title": "IELTS Academic — Writing Task 1",
        "task1_timer_seed": "20:00",
    }


def _fmt_mmss(total_seconds):
    s = max(0, int(total_seconds or 0))
    m = s // 60
    ss = s % 60
    return f"{m:02d}:{ss:02d}"


def _safe_float(v, default=6.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return float(default)


def _task1_feedback_defaults(student_response):
    return {
        "band_score": 6.0,
        "task_achievement": 6.0,
        "coherence_cohesion": 6.0,
        "lexical_resource": 5.5,
        "grammar_accuracy": 6.0,
        "summary": "Clear overall attempt with relevant data. Improve precision and vocabulary range for a higher band.",
        "annotated_text": student_response,
        "task_excerpt": student_response,
        "coherence_excerpt": student_response,
        "lexical_excerpt": student_response,
        "grammar_excerpt": student_response,
        "lexical_quickfixes": [
            "a lot of → the majority of",
            "went up → rose",
            "the data shows → the figures indicate",
        ],
        "task_checks": [
            {"type": "pass", "title": "Overview present", "detail": "You included an overall trend statement."},
            {"type": "fail", "title": "Limited data support", "detail": "Add more exact figures for each comparison."},
            {"type": "warn", "title": "Balance coverage", "detail": "Cover all categories briefly before details."},
        ],
        "coherence_checks": [
            {"type": "pass", "title": "Logical paragraphing", "detail": "Your ideas are mostly grouped clearly."},
            {"type": "fail", "title": "Connector punctuation", "detail": "Some linking phrases need commas."},
            {"type": "warn", "title": "Variety of links", "detail": "Use a wider range of cohesive devices."},
        ],
        "lexical_checks": [
            {"type": "pass", "title": "Topic vocabulary", "detail": "You used relevant transport terms."},
            {"type": "fail", "title": "Informal word choice", "detail": "Replace informal phrases with academic wording."},
            {"type": "warn", "title": "Reporting verbs", "detail": "Vary verbs like shows/indicates/reveals."},
        ],
        "grammar_checks": [
            {"type": "pass", "title": "Sentence control", "detail": "Most sentences are clear and correct."},
            {"type": "fail", "title": "Verb form issues", "detail": "Fix a few tense/form inaccuracies."},
            {"type": "warn", "title": "Complex forms", "detail": "Add more accurate complex clauses."},
        ],
        "task_target": "To reach Band 7: give a clear overview and precise comparisons across all key features.",
        "coherence_target": "To reach Band 7: organise ideas more tightly and improve connector accuracy.",
        "lexical_target": "To reach Band 7: use more precise academic vocabulary and varied reporting verbs.",
        "grammar_target": "To reach Band 7: reduce small grammar errors and show more accurate complex structures.",
        "did_well": [
            "Clear overview sentence identifying the main trend.",
            "Included relevant figures from the chart.",
            "Maintained a logical paragraph sequence.",
        ],
        "improve": [
            "Use more precise academic reporting language.",
            "Add more exact category-by-category comparisons.",
            "Improve punctuation after linking expressions.",
        ],
        "language_suggestions": [
            'Instead of "shows" → use "illustrates"',
            'Instead of "went up a lot" → use "rose significantly"',
            'Instead of "the data shows" → use "the figures indicate"',
        ],
        "model_answer": "Overall, car use remained the dominant mode of commuting in both years, while cycling recorded the largest increase. In 2005, 67% of households travelled to work by car, and this figure rose moderately to 71% by 2015. Public transport also became more common, increasing from 24% to 31%. The most striking shift occurred in bicycle use, which almost doubled from 8% to 15%, suggesting growing interest in sustainable travel. By contrast, walking declined from 18% to 12%, and motorcycle use dropped from 5% to 3%. Taken together, the data indicates that households relied more on cars and public transport in 2015, while less common modes moved in opposite directions.",
    }


def _extract_ann_items(raw):
    red = re.findall(r"<<RED error=\"([^\"]*)\" reason=\"([^\"]*)\">>(.*?)<</RED>>", raw or "", re.S)
    amber = re.findall(r"<<AMBER better=\"([^\"]*)\" reason=\"([^\"]*)\">>(.*?)<</AMBER>>", raw or "", re.S)
    green = re.findall(r"<<GREEN>>(.*?)<</GREEN>>", raw or "", re.S)
    return red, amber, green


def _task1_best_by_question(user):
    best = {}
    rows = WritingTask1Attempt.objects.filter(user=user).values(
        "question_id", "question_type", "band_score"
    )
    for row in rows:
        key = (row["question_type"], row["question_id"])
        band = float(row["band_score"] or 0.0)
        best[key] = max(best.get(key, 0.0), band)
    return best


@login_required
def task1_browser(request):
    best = _task1_best_by_question(request.user)
    cards = []
    for qtype in question_type_list():
        questions = get_questions_by_type(qtype)
        done = sum(1 for q in questions if best.get((qtype, q["id"])))
        cards.append(
            {
                "slug": qtype,
                "name": TYPE_META[qtype]["name"],
                "emoji": TYPE_META[qtype]["emoji"],
                "description": TYPE_META[qtype]["description"],
                "done": done,
                "total": len(questions),
            }
        )
    return render(
        request,
        "writing/task1_browser.html",
        {
            "type_cards": cards,
            "show_submit": False,
            "questions_url": reverse("writing:task1"),
            **_task1_topbar_ctx(),
            **_streak_ctx(request),
        },
    )


@login_required
def task1_question_list(request, question_type):
    if question_type not in TYPE_META:
        raise Http404("Unknown Task 1 type")
    best = _task1_best_by_question(request.user)
    rows = []
    questions = get_questions_by_type(question_type)
    for q in questions:
        best_band = best.get((question_type, q["id"]))
        rows.append(
            {
                "id": q["id"],
                "title": q["title"],
                "prompt_preview": (q["prompt"][:90] + "…") if len(q["prompt"]) > 90 else q["prompt"],
                "best_band": best_band,
            }
        )
    return render(
        request,
        "writing/task1_question_list.html",
        {
            "type_slug": question_type,
            "type_meta": TYPE_META[question_type],
            "rows": rows,
            "show_submit": False,
            "questions_url": reverse("writing:task1"),
            **_task1_topbar_ctx(),
            **_streak_ctx(request),
        },
    )


@login_required
def task1_question_page(request, question_type, question_id):
    blocked = guard_feature(request, FEATURE_WRITING_TASK1)
    if blocked:
        return blocked
    question = get_question(question_type, question_id)
    if not question:
        raise Http404("Question not found")
    prev = request.session.get(f"prev_attempt_{question_id}")
    return render(
        request,
        "writing/task1_question_page.html",
        {
            "type_slug": question_type,
            "type_meta": TYPE_META[question_type],
            "question": question,
            "chart_svg": render_question_chart(question),
            "task_instruction": TASK_INSTRUCTION,
            "show_submit": True,
            "questions_url": reverse("writing:task1_question_list", kwargs={"question_type": question_type}),
            "prev_attempt": prev,
            **_task1_topbar_ctx(),
            **_streak_ctx(request),
        },
    )


def _task1_eval_feedback(question_type_name, prompt_text, student_response, word_count):
    if not settings.OPENAI_API_KEY:
        return _task1_feedback_defaults(student_response)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""You are a fair and experienced IELTS Writing Task 1 examiner.

Question type: {question_type_name}
Task prompt: {prompt_text}
Student response ({word_count} words):
{student_response}

Grade this accurately and fairly. Be encouraging and constructive.

Grading rules:
- 150+ words covering main features = at least Task Achievement 5.5
- Uses data and comparisons = at least 6.0
- Band 5.0 only for responses that seriously misunderstand the task
- Band 7.0 needs: clear overview, accurate data, well-developed comparisons, varied vocabulary

For annotated_text: return the student's COMPLETE response with markers:
- <<GREEN>>phrase<</GREEN>> for well-written phrases (max 3)
- <<RED error="correction" reason="why">>wrong text<</RED>> for errors (max 3)
- <<AMBER better="improved" reason="why">>original<</AMBER>> for vocabulary (max 3)

For each criterion excerpt: return the student's response with only the markers relevant to that criterion.

Return ONLY this JSON with no markdown or backticks:
{{
  "band_score": 5.0-9.0,
  "task_achievement": 5.0-9.0,
  "coherence_cohesion": 5.0-9.0,
  "lexical_resource": 5.0-9.0,
  "grammar_accuracy": 5.0-9.0,
  "summary": "2 sentence overall assessment",
  "annotated_text": "full response with <<GREEN>> <<RED>> <<AMBER>> markers",
  "task_excerpt": "response with task-related markers only",
  "coherence_excerpt": "response with coherence markers only",
  "lexical_excerpt": "response with vocabulary markers only",
  "grammar_excerpt": "response with grammar markers only",
  "lexical_quickfixes": ["original → better", "original → better", "original → better"],
  "task_checks": [{{"type":"pass","title":"...","detail":"..."}}, {{"type":"fail","title":"...","detail":"..."}}, {{"type":"warn","title":"...","detail":"..."}}],
  "coherence_checks": [{{"type":"pass","title":"...","detail":"..."}}, {{"type":"fail","title":"...","detail":"..."}}, {{"type":"warn","title":"...","detail":"..."}}],
  "lexical_checks": [{{"type":"pass","title":"...","detail":"..."}}, {{"type":"fail","title":"...","detail":"..."}}, {{"type":"warn","title":"...","detail":"..."}}],
  "grammar_checks": [{{"type":"pass","title":"...","detail":"..."}}, {{"type":"fail","title":"...","detail":"..."}}, {{"type":"warn","title":"...","detail":"..."}}],
  "task_target": "To reach Band 7: ...",
  "coherence_target": "To reach Band 7: ...",
  "lexical_target": "To reach Band 7: ...",
  "grammar_target": "To reach Band 7: ...",
  "did_well": ["point 1", "point 2", "point 3"],
  "improve": ["point 1", "point 2", "point 3"],
  "language_suggestions": ["Instead of X use Y", "Instead of X use Y", "Instead of X use Y"],
  "model_answer": "Complete Band 7 response 180-200 words"
}}"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are precise, strict, and return JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    raw = completion.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = _extract_json(raw) or {}
    defaults = _task1_feedback_defaults(student_response)
    defaults.update(data or {})
    return defaults


@login_required
def task1_feedback_page(request, question_type, question_id):
    question = get_question(question_type, question_id)
    if not question:
        raise Http404("Question not found")
    if request.method != "POST":
        return redirect("writing:task1_question_page", question_type=question_type, question_id=question_id)

    blocked = guard_feature(request, FEATURE_WRITING_TASK1)
    if blocked:
        return blocked

    response_text = (request.POST.get("response_text") or "").strip()
    word_count = _word_count(response_text)
    time_taken_seconds = int(request.POST.get("time_taken_seconds") or 0)
    if settings.OPENAI_API_KEY:
        err = guard_ai_check(request.user, "writing_task1", will_call_openai=True)
        if err:
            messages.error(request, err)
            return redirect("writing:task1_question_page", question_type=question_type, question_id=question_id)
    payload = _task1_eval_feedback(
        TYPE_META[question_type]["name"],
        question["prompt"],
        response_text,
        word_count,
    )

    def _f(name, default=6.0):
        try:
            return float(payload.get(name, default))
        except (TypeError, ValueError):
            return float(default)

    attempt = WritingTask1Attempt.objects.create(
        user=request.user,
        question_id=question["id"],
        question_type=question_type,
        response_text=response_text,
        word_count=word_count,
        time_taken_seconds=time_taken_seconds,
        band_score=_f("band_score"),
        task_achievement=_f("task_achievement"),
        coherence_cohesion=_f("coherence_cohesion"),
        lexical_resource=_f("lexical_resource"),
        grammar_accuracy=_f("grammar_accuracy"),
        annotated_text=str(payload.get("annotated_text") or ""),
        feedback_json=payload,
    )
    request.session[f"prev_attempt_{question['id']}"] = {
        "band_score": attempt.band_score,
        "word_count": word_count,
        "annotated_html": str(payload.get("annotated_text") or ""),
        "improve": payload.get("improve") or [],
    }
    bump_streak_for_user(request.user)
    return redirect("writing:task1_feedback_page_by_id", question_id=question_id)


@login_required
def task1_feedback_page_by_id(request, question_id):
    all_types = question_type_list()
    question = None
    question_type = None
    for t in all_types:
        q = get_question(t, question_id)
        if q:
            question = q
            question_type = t
            break
    if not question or not question_type:
        raise Http404("Question not found")
    attempt = (
        WritingTask1Attempt.objects.filter(
            user=request.user,
            question_id=question["id"],
            question_type=question_type,
        )
        .order_by("-completed_at")
        .first()
    )
    if not attempt:
        return redirect("writing:task1_question_page", question_type=question_type, question_id=question_id)

    feedback = attempt.feedback_json or _task1_feedback_defaults(attempt.response_text)
    scores = {
        "task_achievement": _safe_float(feedback.get("task_achievement"), attempt.task_achievement),
        "coherence_cohesion": _safe_float(feedback.get("coherence_cohesion"), attempt.coherence_cohesion),
        "lexical_resource": _safe_float(feedback.get("lexical_resource"), attempt.lexical_resource),
        "grammar_accuracy": _safe_float(feedback.get("grammar_accuracy"), attempt.grammar_accuracy),
    }
    weakest_key = min(scores, key=lambda k: scores[k])
    red, amber, green = _extract_ann_items(str(feedback.get("annotated_text") or attempt.annotated_text or ""))

    criteria = []
    for key in ("task_achievement", "coherence_cohesion", "lexical_resource", "grammar_accuracy"):
        meta = CRITERION_META[key]
        score = scores[key]
        criteria.append(
            {
                "key": key,
                "label": meta["label"],
                "color": meta["color"],
                "tag_bg": meta["tag_bg"],
                "score": score,
                "status": "Needs work" if score < 6.0 else "Good",
                "excerpt_raw": str(feedback.get(f"{key.split('_')[0]}_excerpt") or feedback.get(f"{key}_excerpt") or attempt.response_text),
                "checks": feedback.get(f"{key.split('_')[0]}_checks") or feedback.get(f"{key}_checks") or [],
                "target": feedback.get(f"{key.split('_')[0]}_target") or feedback.get(f"{key}_target") or "",
            }
        )

    return render(
        request,
        "writing/task1_feedback_page.html",
        {
            "type_slug": question_type,
            "type_meta": TYPE_META[question_type],
            "question": question,
            "attempt": attempt,
            "feedback": feedback,
            "criteria": criteria,
            "weakest_key": weakest_key,
            "weakest_label": CRITERION_META[weakest_key]["label"],
            "weakest_score": scores[weakest_key],
            "ann_error_count": len(red),
            "ann_improve_count": len(amber),
            "ann_good_count": len(green),
            "time_used_mmss": _fmt_mmss(attempt.time_taken_seconds),
            "show_submit": False,
            "show_try_again_top": user_can(request.user, FEATURE_WRITING_TASK1),
            "questions_url": reverse("writing:task1_question_list", kwargs={"question_type": question_type}),
            "try_again_url": reverse("writing:task1_question_page", kwargs={"question_type": question_type, "question_id": question["id"]}) if user_can(request.user, FEATURE_WRITING_TASK1) else "",
            **_task1_topbar_ctx(),
            **_streak_ctx(request),
        },
    )


def _task2_questions_by_type(essay_type):
    return [q for q in TASK2_QUESTIONS if q["type"] == essay_type]


def _task2_get_question(essay_type, qid):
    for q in TASK2_QUESTIONS:
        if q["type"] == essay_type and int(q["id"]) == int(qid):
            return q
    return None


def _best_task2_by_question(user):
    best = {}
    for row in WritingTask2Attempt.objects.filter(user=user).values("question_id", "essay_type", "band_score"):
        key = (row["essay_type"], row["question_id"])
        best[key] = max(best.get(key, 0.0), float(row["band_score"] or 0.0))
    return best


def _latest_attempts(user, limit=3):
    t1 = [
        {
            "task": "Task 1",
            "score": a.band_score,
            "word_count": a.word_count,
            "when": a.completed_at,
            "title": f"{a.question_type} · Q{a.question_id}",
            "feedback_url": redirect(
                "writing:task1_feedback_page_by_id", question_id=a.question_id
            ).url,
        }
        for a in WritingTask1Attempt.objects.filter(user=user).order_by("-completed_at")[:limit]
    ]
    t2 = [
        {
            "task": "Task 2",
            "score": a.band_score,
            "word_count": a.word_count,
            "when": a.completed_at,
            "title": f"{a.essay_type} · Q{a.question_id}",
            "feedback_url": redirect(
                "writing:task2_feedback_page", essay_type=a.essay_type, q_id=a.question_id
            ).url,
        }
        for a in WritingTask2Attempt.objects.filter(user=user).order_by("-completed_at")[:limit]
    ]
    rows = sorted(t1 + t2, key=lambda x: x["when"], reverse=True)
    return rows[:limit]


@login_required
def writing_home(request):
    user = request.user
    t1_best = (
        WritingTask1Attempt.objects.filter(user=user)
        .order_by("-band_score")
        .values_list("band_score", flat=True)
        .first()
    )
    t2_best = (
        WritingTask2Attempt.objects.filter(user=user)
        .order_by("-band_score")
        .values_list("band_score", flat=True)
        .first()
    )
    lesson_done = LessonProgress.objects.filter(user=user).values("lesson_id").distinct().count()
    grammar_done = (
        GrammarTopicProgress.objects.filter(user=user).values("topic_id").distinct().count()
    )
    return render(
        request,
        "writing/writing_hub.html",
        {
            "task1_best": t1_best,
            "task2_best": t2_best,
            "recent_attempts": _latest_attempts(user),
            "lesson_done": lesson_done,
            "lesson_total": len(LESSONS),
            "grammar_done": grammar_done,
            "grammar_total": len(GRAMMAR_TOPICS),
            **_streak_ctx(request),
        },
    )


@login_required
def task2_browser(request):
    best = _best_task2_by_question(request.user)
    cards = []
    for t, meta in TASK2_TYPE_META.items():
        qs = _task2_questions_by_type(t)
        done = sum(1 for q in qs if best.get((t, q["id"])))
        cards.append({"slug": t, "name": meta["name"], "emoji": meta["emoji"], "description": meta["description"], "done": done, "total": len(qs)})
    return render(
        request,
        "writing/task2_browser.html",
        {"type_cards": cards, "show_submit": False, "task1_topbar_title": "IELTS Academic — Writing Task 2", "task1_timer_seed": "40:00", "questions_url": reverse("writing:task2"), **_streak_ctx(request)},
    )


@login_required
def task2_question_list(request, essay_type):
    if essay_type not in TASK2_TYPE_META:
        raise Http404("Unknown Task 2 type")
    best = _best_task2_by_question(request.user)
    rows = []
    for q in _task2_questions_by_type(essay_type):
        band = best.get((essay_type, q["id"]))
        rows.append({"id": q["id"], "title": q["title"], "prompt_preview": (q["prompt"][:90] + "…") if len(q["prompt"]) > 90 else q["prompt"], "best_band": band})
    return render(
        request,
        "writing/task2_question_list.html",
        {"essay_type": essay_type, "type_meta": TASK2_TYPE_META[essay_type], "rows": rows, "show_submit": False, "task1_topbar_title": "IELTS Academic — Writing Task 2", "task1_timer_seed": "40:00", "questions_url": reverse("writing:task2"), **_streak_ctx(request)},
    )


@login_required
def task2_question_page(request, essay_type, q_id):
    blocked = guard_feature(request, FEATURE_WRITING_TASK2)
    if blocked:
        return blocked
    q = _task2_get_question(essay_type, q_id)
    if not q:
        raise Http404("Question not found")
    prev = request.session.get(f"prev_attempt_{q_id}")
    return render(
        request,
        "writing/task2_question_page.html",
        {
            "essay_type": essay_type,
            "type_meta": TASK2_TYPE_META[essay_type],
            "question": q,
            "show_submit": True,
            "task1_topbar_title": "IELTS Academic — Writing Task 2",
            "task1_timer_seed": "40:00",
            "questions_url": reverse("writing:task2_question_list", kwargs={"essay_type": essay_type}),
            "prev_attempt": prev,
            **_streak_ctx(request),
        },
    )


def _task2_feedback_defaults(text):
    d = _task1_feedback_defaults(text)
    d["task_response"] = d.pop("task_achievement", 6.0)
    d["task_response_checks"] = d.pop("task_checks", [])
    d["task_response_target"] = d.pop("task_target", "")
    return d


def _task2_eval_feedback(essay_type_name, prompt_text, student_response, word_count):
    if not settings.OPENAI_API_KEY:
        return _task2_feedback_defaults(student_response)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""You are a fair IELTS Academic Writing Task 2 examiner.

Essay type: {essay_type_name}
Prompt: {prompt_text}
Student response ({word_count} words):
{student_response}

Grading rules:
- Full question answered, clear position, both parts addressed where required, and specific examples.
- Use <<GREEN>>, <<RED error=".." reason="..">>, <<AMBER better=".." reason="..">> markers same as Task 1.
- Return strict JSON with task_response instead of task_achievement and the same other fields.
"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": "Return strict JSON only."}, {"role": "user", "content": prompt}],
    )
    raw = completion.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = _extract_json(raw) or {}
    defaults = _task2_feedback_defaults(student_response)
    defaults.update(data or {})
    return defaults


@login_required
def task2_feedback_page(request, essay_type, q_id):
    q = _task2_get_question(essay_type, q_id)
    if not q:
        raise Http404("Question not found")
    if request.method != "POST":
        attempt = WritingTask2Attempt.objects.filter(user=request.user, essay_type=essay_type, question_id=q_id).order_by("-completed_at").first()
        if not attempt:
            return redirect("writing:task2_question_page", essay_type=essay_type, q_id=q_id)
    else:
        blocked = guard_feature(request, FEATURE_WRITING_TASK2)
        if blocked:
            return blocked
        txt = (request.POST.get("response_text") or "").strip()
        wc = _word_count(txt)
        tsec = int(request.POST.get("time_taken_seconds") or 0)
        if settings.OPENAI_API_KEY:
            err = guard_ai_check(request.user, "writing_task2", will_call_openai=True)
            if err:
                messages.error(request, err)
                return redirect("writing:task2_question_page", essay_type=essay_type, q_id=q_id)
        feedback = _task2_eval_feedback(TASK2_TYPE_META[essay_type]["name"], q["prompt"], txt, wc)
        attempt = WritingTask2Attempt.objects.create(
            user=request.user,
            question_id=q_id,
            essay_type=essay_type,
            response_text=txt,
            word_count=wc,
            time_taken_seconds=tsec,
            band_score=_safe_float(feedback.get("band_score")),
            task_response=_safe_float(feedback.get("task_response")),
            coherence_cohesion=_safe_float(feedback.get("coherence_cohesion")),
            lexical_resource=_safe_float(feedback.get("lexical_resource")),
            grammar_accuracy=_safe_float(feedback.get("grammar_accuracy")),
            annotated_text=str(feedback.get("annotated_text") or ""),
            feedback_json=feedback,
        )
        request.session[f"prev_attempt_{q_id}"] = {
            "band_score": attempt.band_score,
            "word_count": wc,
            "annotated_html": str(feedback.get("annotated_text") or ""),
            "improve": feedback.get("improve") or [],
        }
        bump_streak_for_user(request.user)
    feedback = attempt.feedback_json or _task2_feedback_defaults(attempt.response_text)
    scores = {
        "task_response": _safe_float(feedback.get("task_response"), attempt.task_response),
        "coherence_cohesion": _safe_float(feedback.get("coherence_cohesion"), attempt.coherence_cohesion),
        "lexical_resource": _safe_float(feedback.get("lexical_resource"), attempt.lexical_resource),
        "grammar_accuracy": _safe_float(feedback.get("grammar_accuracy"), attempt.grammar_accuracy),
    }
    weakest_key = min(scores, key=lambda k: scores[k])
    criteria = []
    for key in ("task_response", "coherence_cohesion", "lexical_resource", "grammar_accuracy"):
        meta = CRITERION_META.get(key.replace("task_response", "task_achievement"), CRITERION_META["coherence_cohesion"])
        criteria.append({"key": key, "label": "Task Response" if key == "task_response" else meta["label"], "color": meta["color"], "tag_bg": meta["tag_bg"], "score": scores[key], "status": "Needs work" if scores[key] < 6 else "Good", "checks": feedback.get(f"{key.split('_')[0]}_checks") or feedback.get(f"{key}_checks") or [], "target": feedback.get(f"{key.split('_')[0]}_target") or feedback.get(f"{key}_target") or ""})
    return render(
        request,
        "writing/task2_feedback_page.html",
        {
            "essay_type": essay_type,
            "type_meta": TASK2_TYPE_META[essay_type],
            "question": q,
            "attempt": attempt,
            "feedback": feedback,
            "criteria": criteria,
            "weakest_key": weakest_key,
            "weakest_label": "Task Response" if weakest_key == "task_response" else CRITERION_META[weakest_key]["label"],
            "weakest_score": scores[weakest_key],
            "time_used_mmss": _fmt_mmss(attempt.time_taken_seconds),
            "show_submit": False,
            "show_try_again_top": user_can(request.user, FEATURE_WRITING_TASK2),
            "task1_topbar_title": "IELTS Academic — Writing Task 2",
            "task1_timer_seed": "40:00",
            "questions_url": reverse("writing:task2_question_list", kwargs={"essay_type": essay_type}),
            "try_again_url": reverse("writing:task2_question_page", kwargs={"essay_type": essay_type, "q_id": q["id"]}) if user_can(request.user, FEATURE_WRITING_TASK2) else "",
            **_streak_ctx(request),
        },
    )


@login_required
def lessons_hub(request):
    blocked = guard_feature(request, FEATURE_WRITING_LESSONS)
    if blocked:
        return blocked
    done_ids = set(LessonProgress.objects.filter(user=request.user).values_list("lesson_id", flat=True))
    t1 = [l for l in LESSONS if l["task"] == "task1"]
    t2 = [l for l in LESSONS if l["task"] == "task2"]
    return render(
        request,
        "writing/lessons_hub.html",
        {
            "task1_lessons": t1,
            "task2_lessons": t2,
            "done_ids": done_ids,
            "lesson_done": len(done_ids),
            "lesson_total": len(LESSONS),
            **_streak_ctx(request),
        },
    )


def _lesson_practice_feedback_defaults():
    return {
        "ready": False,
        "what_you_did_well": ["You attempted the task — keep practising."],
        "mistakes_and_fixes": [],
        "how_to_improve": ["Review the lesson and try again with a clearer focus on the target skill."],
        "model_answer": "",
    }


def _lesson_practice_eval(lesson, practice, student_response, word_count):
    defaults = _lesson_practice_feedback_defaults()
    if not settings.OPENAI_API_KEY:
        return defaults

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"""You are an experienced IELTS Writing examiner.

Lesson: {lesson["title"]}
Skill to assess (ONLY this skill — ignore other aspects): {practice["skill_focus"]}

Practice task for the student:
{practice["instruction"]}

Source material / prompt:
{practice["prompt_context"]}

Student answer ({word_count} words):
{student_response}

Evaluate ONLY whether the student demonstrated the skill this lesson teaches. Be fair and constructive.
- "ready": true only if there are NO major mistakes for this specific skill (minor wording issues are OK).
- "ready": false if there are significant errors in the target skill (e.g. overview with too much detail, intro with data, weak thesis, missing TEEL structure).

Return ONLY valid JSON with no markdown:
{{
  "ready": true or false,
  "what_you_did_well": ["1-3 specific strengths"],
  "mistakes_and_fixes": [
    {{"problem": "exact quote from student text", "why": "why it is a problem for this skill", "corrected": "improved version"}}
  ],
  "how_to_improve": ["1-2 concrete actionable suggestions"],
  "model_answer": "A Band 7+ model answer for this exact practice task only"
}}"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are precise, fair, and return JSON only."},
                {"role": "user", "content": prompt},
            ],
        )
        raw = completion.choices[0].message.content or "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = _extract_json(raw) or {}
        defaults.update(data or {})
        defaults["ready"] = bool(defaults.get("ready"))
        defaults["what_you_did_well"] = list(defaults.get("what_you_did_well") or [])[:3]
        defaults["mistakes_and_fixes"] = list(defaults.get("mistakes_and_fixes") or [])
        defaults["how_to_improve"] = list(defaults.get("how_to_improve") or [])[:2]
        defaults["model_answer"] = str(defaults.get("model_answer") or "")
        return defaults
    except Exception:
        return None


@login_required
def lesson_detail(request, lesson_id):
    blocked = guard_feature(request, FEATURE_WRITING_LESSONS)
    if blocked:
        return blocked
    lesson = next((l for l in LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise Http404("Lesson not found")
    practice = get_lesson_practice(lesson_id)
    if not practice:
        raise Http404("Practice task not found")
    lecture = get_lesson_lecture(lesson_id)
    if not lecture:
        raise Http404("Lesson content not found")
    attempts = list(
        LessonPracticeAttempt.objects.filter(user=request.user, lesson_id=lesson_id).order_by("-attempt_number")
    )
    is_complete = LessonProgress.objects.filter(user=request.user, lesson_id=lesson_id).exists()
    latest = attempts[0] if attempts else None
    return render(
        request,
        "writing/lesson_detail.html",
        {
            "lesson": lesson,
            "lecture": lecture,
            "practice": practice,
            "attempts": attempts,
            "latest_attempt": latest,
            "is_complete": is_complete,
            "lesson_total": len(LESSONS),
            **_streak_ctx(request),
        },
    )


@login_required
@require_POST
def lesson_practice_check(request, lesson_id):
    blocked = guard_feature(request, FEATURE_WRITING_LESSONS, json_response=True)
    if blocked:
        return blocked
    lesson = next((l for l in LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return JsonResponse({"ok": False, "error": "Lesson not found."}, status=404)
    practice = get_lesson_practice(lesson_id)
    if not practice:
        return JsonResponse({"ok": False, "error": "Practice task not found."}, status=404)

    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        body = {}
    response_text = (body.get("response_text") or "").strip()
    word_count = _word_count(response_text)
    if word_count < 5:
        return JsonResponse({"ok": False, "error": "Write at least 5 words before checking."}, status=400)

    if settings.OPENAI_API_KEY:
        err = guard_ai_check(request.user, "lesson_practice", will_call_openai=True)
        if err:
            return ai_limit_json()

    feedback = _lesson_practice_eval(lesson, practice, response_text, word_count)
    if feedback is None:
        return JsonResponse({"ok": False, "error": "Couldn't check your answer. Try again."}, status=502)

    last_num = (
        LessonPracticeAttempt.objects.filter(user=request.user, lesson_id=lesson_id)
        .order_by("-attempt_number")
        .values_list("attempt_number", flat=True)
        .first()
    ) or 0
    attempt = LessonPracticeAttempt.objects.create(
        user=request.user,
        lesson_id=lesson_id,
        attempt_number=last_num + 1,
        response_text=response_text,
        word_count=word_count,
        ready=bool(feedback.get("ready")),
        feedback_json=feedback,
    )
    completed = False
    if attempt.ready:
        LessonProgress.objects.get_or_create(user=request.user, lesson_id=lesson_id)
        completed = True

    return JsonResponse(
        {
            "ok": True,
            "attempt_number": attempt.attempt_number,
            "word_count": word_count,
            "ready": attempt.ready,
            "completed": completed,
            "feedback": feedback,
        }
    )


@login_required
def grammar_hub(request):
    blocked = guard_feature(request, FEATURE_WRITING_GRAMMAR)
    if blocked:
        return blocked
    done_ids = set(
        GrammarTopicProgress.objects.filter(user=request.user).values_list("topic_id", flat=True)
    )
    return render(
        request,
        "writing/grammar_hub.html",
        {
            "topics": GRAMMAR_TOPICS,
            "done_ids": done_ids,
            "grammar_done": len(done_ids),
            "grammar_total": len(GRAMMAR_TOPICS),
            **_streak_ctx(request),
        },
    )


@login_required
def grammar_topic(request, topic_id):
    blocked = guard_feature(request, FEATURE_WRITING_GRAMMAR)
    if blocked:
        return blocked
    topic = get_grammar_topic(topic_id)
    if not topic:
        raise Http404("Grammar topic not found")
    GrammarTopicProgress.objects.get_or_create(user=request.user, topic_id=topic_id)
    done_ids = set(
        GrammarTopicProgress.objects.filter(user=request.user).values_list("topic_id", flat=True)
    )
    topic_ids = [t["id"] for t in GRAMMAR_TOPICS]
    idx = topic_ids.index(topic_id)
    prev_topic = GRAMMAR_TOPICS[idx - 1] if idx > 0 else None
    next_topic = GRAMMAR_TOPICS[idx + 1] if idx < len(GRAMMAR_TOPICS) - 1 else None
    return render(
        request,
        "writing/grammar_topic.html",
        {
            "topic": topic,
            "is_done": topic_id in done_ids,
            "grammar_done": len(done_ids),
            "grammar_total": len(GRAMMAR_TOPICS),
            "prev_topic": prev_topic,
            "next_topic": next_topic,
            **_streak_ctx(request),
        },
    )


@login_required
def grammar_mistakes(request):
    blocked = guard_feature(request, FEATURE_WRITING_GRAMMAR)
    if blocked:
        return blocked
    from boostingscore.review_schedule import mark_section_reviewed
    from .grammar_mistakes_content import GRAMMAR_MISTAKES, SELF_CHECK_ITEMS

    mark_section_reviewed(request.user, "writing_grammar")
    return render(
        request,
        "writing/grammar_mistakes.html",
        {
            "mistakes": GRAMMAR_MISTAKES,
            "checklist": SELF_CHECK_ITEMS,
            **_streak_ctx(request),
        },
    )


@login_required
def skills_hub(request):
    done_ids = set(SkillProgress.objects.filter(user=request.user).values_list("skill_id", flat=True))
    latest_t1 = WritingTask1Attempt.objects.filter(user=request.user).order_by("-completed_at").first()
    latest_t2 = WritingTask2Attempt.objects.filter(user=request.user).order_by("-completed_at").first()
    weakest = None
    if latest_t1 and (not latest_t2 or latest_t1.completed_at >= latest_t2.completed_at):
        fb = latest_t1.feedback_json or {}
        scores = {"task_achievement": _safe_float(fb.get("task_achievement"), latest_t1.task_achievement), "coherence_cohesion": _safe_float(fb.get("coherence_cohesion"), latest_t1.coherence_cohesion), "lexical_resource": _safe_float(fb.get("lexical_resource"), latest_t1.lexical_resource), "grammar_accuracy": _safe_float(fb.get("grammar_accuracy"), latest_t1.grammar_accuracy)}
        weakest = min(scores, key=scores.get)
    elif latest_t2:
        fb = latest_t2.feedback_json or {}
        scores = {"task_response": _safe_float(fb.get("task_response"), latest_t2.task_response), "coherence_cohesion": _safe_float(fb.get("coherence_cohesion"), latest_t2.coherence_cohesion), "lexical_resource": _safe_float(fb.get("lexical_resource"), latest_t2.lexical_resource), "grammar_accuracy": _safe_float(fb.get("grammar_accuracy"), latest_t2.grammar_accuracy)}
        weakest = min(scores, key=scores.get)
    rec = SKILL_MAP.get(weakest, []) if weakest else []
    rec_skills = [s for s in SKILLS if s["id"] in rec]
    return render(request, "writing/skills_hub.html", {"skills": SKILLS, "done_ids": done_ids, "recommended": rec_skills, "weakest": weakest, **_streak_ctx(request)})


@login_required
def skill_detail(request, skill_id):
    skill = next((s for s in SKILLS if s["id"] == skill_id), None)
    if not skill:
        raise Http404("Skill not found")
    if request.method == "POST" and request.POST.get("mark_done") == "1":
        SkillProgress.objects.get_or_create(user=request.user, skill_id=skill_id)
        return redirect("writing:skill_detail", skill_id=skill_id)
    from_feedback = request.GET.get("from_feedback") == "1"
    criterion = request.GET.get("criterion") or ""
    return render(request, "writing/skill_detail.html", {"skill": skill, "from_feedback": from_feedback, "criterion": criterion, **_streak_ctx(request)})
