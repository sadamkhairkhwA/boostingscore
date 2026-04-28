import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from openai import OpenAI

from .academic_test_data import band_from_score, get_client_test_payload, score_answers
from .models import (
    GeneralReadingArticle,
    GeneralReadingBookmark,
    GeneralReadingSession,
    GeneralReadingSummary,
    IELTSTestResult,
    ReadingAttempt,
    ReadingTest,
    ReadingTestResult,
)

openai_api_key = settings.OPENAI_API_KEY

IELTS_TESTS = [
    {
        "id": 1,
        "title": "Local services & travel",
        "band": "5.0–5.5",
        "types": "MC · T/F/NG · Gap-fill · Yes/No/NG",
        "desc": "Short notices and direct detail matching.",
        "available": True,
    },
    {
        "id": 2,
        "title": "Digital services & health",
        "band": "5.5–6.0",
        "types": "MC · T/F/NG · Y/N/NG · Sentence fill",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 3,
        "title": "Transport & environment",
        "band": "6.0–6.5",
        "types": "MC · T/F/NG · Gap-fill · Match headings",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 4,
        "title": "Culture & funding",
        "band": "6.5–7.0",
        "types": "MC · T/F/NG · Y/N/NG · Short answer",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 5,
        "title": "Science & policy",
        "band": "7.0–7.5",
        "types": "MC · T/F/NG · Gap-fill · Match headings",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 6,
        "title": "Law & digital proceedings",
        "band": "7.5–8.0",
        "types": "MC · T/F/NG · Y/N/NG · Sentence fill",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 7,
        "title": "Economics & trade",
        "band": "8.0–8.5",
        "types": "MC · T/F/NG · Gap-fill · Match headings",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 8,
        "title": "Medicine & research",
        "band": "8.5–9.0",
        "types": "MC · T/F/NG · Y/N/NG · Short answer",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 9,
        "title": "Mixed topics — timed sim",
        "band": "Mixed",
        "types": "All 6 question types mixed",
        "desc": "Coming soon.",
        "available": False,
    },
    {
        "id": 10,
        "title": "Full mock exam — Band 9",
        "band": "9.0",
        "types": "All types · maximum difficulty",
        "desc": "Coming soon.",
        "available": False,
    },
]

TEST_1 = IELTS_TESTS[0]


def get_streak(user):
    return getattr(getattr(user, "profile", None), "streak", 0) or 0


def _streak_ctx(request):
    return {"streak": get_streak(request.user)}


def build_ielts_prompt():
    return """You are an expert IELTS Academic reading test writer.

Create ONE complete IELTS Academic Reading practice test on the topic: "Local services and travel" at Band 5.0–5.5 difficulty.

Output ONLY valid JSON (no markdown fences) with this exact top-level shape:
{
  "test_title": string,
  "band": "5.0-5.5",
  "parts": [
    {
      "part_number": 1,
      "passage_title": string,
      "passage_paragraphs": [ { "label": "A", "text": string }, ... at least 5 paragraphs ],
      "questions": [ ... exactly 13 questions ... ]
    },
    {
      "part_number": 2,
      "passage_title": string,
      "passage_paragraphs": [ { "label": "A", "text": string }, ... ],
      "questions": [ ... exactly 13 questions ... ]
    },
    {
      "part_number": 3,
      "passage_title": string,
      "passage_paragraphs": [ { "label": "A", "text": string }, ... ],
      "questions": [ ... exactly 14 questions ... ]
    }
  ]
}

Question object schema (every question MUST include these keys):
- "id": integer from 1 to 40 in order across the whole test (no gaps)
- "type": one of:
  "match_paragraph" | "tfng" | "gap" | "mc" | "ynng" | "sentence" | "match_heading"
- "prompt": string (the question text / statement / instruction)
- "options": array of strings (for MC: 4 options A-D as strings; for TFNG/YNNG: exactly ["True","False","Not Given"] or ["Yes","No","Not Given"] as appropriate)
- "correct": string (the single correct answer text EXACTLY matching one option, or the paragraph letter for match types, etc.)

Type counts MUST be EXACTLY:
Part 1 (13): match_paragraph x5, tfng x4, gap x4
Part 2 (13): mc x4, ynng x5, sentence x4
Part 3 (14): match_heading x5, tfng x5, mc x4

Rules:
- For "match_paragraph": options are paragraph letters like ["A","B","C","D","E"] and "correct" is one letter.
- For "match_heading": provide a list of headings in "options" and "correct" is the correct heading string.
- For "gap": "prompt" includes numbered gaps like (14) and "options" lists possible words/phrases; "correct" matches one option string.
- For "sentence": sentence completion with options; "correct" matches one option.
- Use realistic IELTS wording; keep vocabulary appropriate for Band 5.0–5.5.
"""


def _norm_type(t):
    if not t:
        return ""
    return str(t).strip().lower()


def validate_test_content(data):
    """Validate 3 parts with 13+13+14 questions and required type counts."""
    try:
        parts = data["parts"]
    except (KeyError, TypeError):
        return False, "Missing parts array."

    if not isinstance(parts, list) or len(parts) != 3:
        return False, "Must have exactly 3 parts."

    expected = [
        {"match_paragraph": 5, "tfng": 4, "gap": 4},
        {"mc": 4, "ynng": 5, "sentence": 4},
        {"match_heading": 5, "tfng": 5, "mc": 4},
    ]

    all_ids = []
    for idx, part in enumerate(parts):
        qs = part.get("questions")
        if not isinstance(qs, list):
            return False, f"Part {idx+1} questions invalid."
        counts = Counter(_norm_type(q.get("type")) for q in qs)
        for k, v in expected[idx].items():
            if counts.get(k, 0) != v:
                return False, f"Part {idx+1} type counts mismatch for {k}: expected {v}, got {counts.get(k,0)}."
        for q in qs:
            if "id" not in q or "correct" not in q:
                return False, "Each question needs id and correct."
            all_ids.append(int(q["id"]))

    if len(all_ids) != 40 or sorted(all_ids) != list(range(1, 41)):
        return False, "Question ids must be 1..40 unique."

    return True, ""


def _extract_json(text):
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}\s*$", text)
        if not m:
            return None
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            return None


def _strip_correct_from_parts(parts):
    out = []
    for part in parts:
        p = dict(part)
        qs = []
        for q in part.get("questions", []):
            qc = dict(q)
            qc.pop("correct", None)
            qs.append(qc)
        p["questions"] = qs
        out.append(p)
    return out


def _answer_map_from_parts(parts):
    m = {}
    for part in parts:
        for q in part.get("questions", []):
            qid = str(int(q["id"]))
            m[qid] = str(q.get("correct", "")).strip()
    return m


@login_required
def reading_home(request):
    user = request.user
    streak = get_streak(user)
    sessions_done = overall_avg = ielts_done = ielts_avg = 0
    try:
        attempts = ReadingAttempt.objects.filter(student=user, completed=True)
        sessions_done = attempts.count()
        scores = [a.score for a in attempts if a.score is not None]
        overall_avg = round(sum(scores) / len(scores), 1) if scores else 0
        ielts_attempts = attempts.filter(test_type="ielts")
        ielts_done = ielts_attempts.count()
        ielts_scores = [a.score for a in ielts_attempts if a.score is not None]
        ielts_avg = round(sum(ielts_scores) / len(ielts_scores), 1) if ielts_scores else 0
    except Exception:
        pass

    return render(
        request,
        "reading/reading_home.html",
        {
            "tests": IELTS_TESTS,
            "streak": streak,
            "sessions_done": sessions_done,
            "overall_avg": overall_avg,
            "ielts_done": ielts_done,
            "ielts_avg": ielts_avg,
            **_streak_ctx(request),
        },
    )


@login_required
def ielts_home(request):
    return render(
        request,
        "reading/ielts_home.html",
        {
            "tests": IELTS_TESTS,
            "streak": get_streak(request.user),
            **_streak_ctx(request),
        },
    )


@login_required
def ielts_exam(request):
    candidate_name = request.user.get_full_name() or request.user.username
    return render(
        request,
        "reading/ielts_exam.html",
        {
            "test": TEST_1,
            "streak": get_streak(request.user),
            "candidate_name": candidate_name,
            **_streak_ctx(request),
        },
    )


@login_required
@require_POST
def generate_ielts_test(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"ok": False, "error": "OpenAI API key is not configured."}, status=503)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def call_model():
        completion = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=8000,
            temperature=0.35,
            messages=[
                {"role": "system", "content": "You write IELTS Academic reading tests as strict JSON only."},
                {"role": "user", "content": build_ielts_prompt()},
            ],
        )
        return completion.choices[0].message.content or ""

    raw = call_model()
    data = _extract_json(raw)
    ok, err = (False, "parse")
    if isinstance(data, dict):
        ok, err = validate_test_content(data)
    if not ok:
        raw2 = call_model()
        data = _extract_json(raw2)
        if isinstance(data, dict):
            ok, err = validate_test_content(data)

    if not ok or not isinstance(data, dict):
        return JsonResponse({"ok": False, "error": f"Invalid test content: {err}"}, status=422)

    parts = data["parts"]
    answer_key = _answer_map_from_parts(parts)
    client_parts = _strip_correct_from_parts(parts)
    payload = {
        "test_title": data.get("test_title") or "IELTS Reading",
        "band": data.get("band") or "5.0-5.5",
        "parts": client_parts,
    }
    request.session["ielts_answer_key"] = answer_key
    request.session["ielts_test_title"] = payload["test_title"]
    return JsonResponse({"ok": True, "test": payload})


@login_required
@require_POST
def submit_ielts_test(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    answers = body.get("answers") or {}
    time_taken = int(body.get("time_taken_secs") or 0)
    key = request.session.get("ielts_answer_key") or {}
    if not key:
        return JsonResponse({"ok": False, "error": "No active test session. Regenerate the test."}, status=400)

    correct = 0
    for qid, exp in key.items():
        got = str(answers.get(qid, "")).strip()
        if got.lower() == str(exp).strip().lower():
            correct += 1
        elif got.lower() in ("t", "true") and str(exp).strip().lower() in ("true", "t"):
            correct += 1
        elif got.lower() in ("f", "false") and str(exp).strip().lower() in ("false", "f"):
            correct += 1
        elif got.lower() in ("ng", "n/g", "not given") and "not given" in str(exp).strip().lower():
            correct += 1

    band = "5.0"
    pct = correct / 40.0 if 40 else 0
    if pct >= 0.9:
        band = "8.5–9.0"
    elif pct >= 0.8:
        band = "7.5–8.0"
    elif pct >= 0.7:
        band = "6.5–7.0"
    elif pct >= 0.55:
        band = "6.0–6.5"
    else:
        band = "5.0–5.5"

    title = request.session.get("ielts_test_title") or TEST_1["title"]
    try:
        IELTSTestResult.objects.create(
            student=request.user,
            test_id=1,
            test_title=title,
            band=band,
            score=correct,
            total_questions=40,
            time_taken_secs=time_taken,
            answers_json=answers,
        )
        ReadingAttempt.objects.create(
            student=request.user,
            test_type="ielts",
            score=float(correct),
            total_questions=40,
            correct_answers=correct,
            time_taken_secs=time_taken,
            completed=True,
        )
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=500)

    request.session.pop("ielts_answer_key", None)
    request.session.pop("ielts_test_title", None)

    from vocabulary.streak_utils import bump_streak_for_user

    bump_streak_for_user(request.user)

    return JsonResponse(
        {
            "ok": True,
            "score": correct,
            "total": 40,
            "band": band,
            "answers_key": key,
        }
    )


READING_QUESTION_TYPES = [
    {
        "title": "True / False / Not Given",
        "badges": [("TFNG", "tfng"), ("Core", "core")],
        "how": (
            "A statement is given. You find if the passage directly supports it (True), "
            "directly contradicts it (False), or simply does not address it (Not Given). "
            "The answer must come from the text — not your knowledge."
        ),
        "focus": "Locating specific factual claims and distinguishing what is said vs what is not said",
        "mistakes": [
            "Choosing False when the passage just does not mention it.",
            "Using outside knowledge to answer.",
            "Spending too long looking for something that is not there.",
        ],
        "confusing": (
            "The difference between False and Not Given. False means the passage says the "
            "opposite. Not Given means the topic is absent entirely — the passage neither "
            "confirms nor denies it."
        ),
    },
    {
        "title": "Yes / No / Not Given",
        "badges": [("Y/N/NG", "tfng"), ("Opinion", "opinion")],
        "how": (
            "Same structure as TFNG but the statements are about the writer's opinion, claims, "
            "or views — not facts. Look for opinion language: argues, believes, suggests, "
            "claims, insists."
        ),
        "focus": "Identifying the writer's stance and distinguishing stated opinion from absence of opinion",
        "mistakes": [
            "Treating it like TFNG (looking for facts instead of opinions).",
            'Missing hedging language like "could" or "might" which makes an answer Not Given.',
            "Assuming the writer agrees with something just because they describe it.",
        ],
        "confusing": (
            'Writers often describe a viewpoint without agreeing with it. "The author discusses '
            'the benefits of X" does not mean the author supports X.'
        ),
    },
    {
        "title": "Matching headings",
        "badges": [("Matching", "matching"), ("Heading", "heading")],
        "how": (
            "A list of headings is given. You match each heading to the correct paragraph. "
            "The heading must match the main idea of the whole paragraph — not just one sentence."
        ),
        "focus": "Understanding paragraph structure and identifying the central topic",
        "mistakes": [
            "Matching a heading to a detail mentioned in the paragraph, not the main idea.",
            "Being misled by a word in the heading that also appears in the paragraph.",
            "Not eliminating headings already used.",
        ],
        "confusing": (
            "A heading may contain a keyword that also appears in the paragraph — but still be "
            "wrong if it only matches one small detail. The heading must represent the whole paragraph."
        ),
    },
    {
        "title": "Matching information",
        "badges": [("Matching", "matching"), ("Core", "core")],
        "how": (
            "You match statements or pieces of information to the paragraph (A, B, C...) where "
            "they appear. Paragraphs can be used more than once."
        ),
        "focus": "Scanning for specific details across multiple paragraphs quickly",
        "mistakes": [
            "Reading every paragraph in full for each question — too slow.",
            "Assuming each paragraph is only used once.",
            "Getting distracted by similar-sounding information in the wrong paragraph.",
        ],
        "confusing": (
            "Paragraphs can be used more than once and some paragraphs may not be used at all. "
            "This confuses test takers who try to use each letter exactly once."
        ),
    },
    {
        "title": "Matching features",
        "badges": [("Matching", "matching"), ("Core", "core")],
        "how": (
            "Match names, dates, or items in column A to descriptions or sentence endings in "
            "column B. Often involves matching researchers, countries, or findings."
        ),
        "focus": "Understanding relationships and details — who said what, what goes with what",
        "mistakes": [
            "Matching based on proximity — answer is near the name in the passage so must be right.",
            "Not reading all options before choosing.",
            "Ignoring the instruction about whether options can be used more than once.",
        ],
        "confusing": (
            "The correct answer for a name/item is often NOT in the same sentence as that name "
            "in the passage — you need to read the surrounding context carefully."
        ),
    },
    {
        "title": "Gap-fill",
        "badges": [("Gap", "gap"), ("Core", "core")],
        "how": (
            "Complete sentences or a summary using words from the passage. The word limit is "
            'strict — usually "NO MORE THAN TWO WORDS AND/OR A NUMBER." Copy spelling exactly '
            "from the passage."
        ),
        "focus": "Scanning for specific information and understanding paraphrase",
        "mistakes": [
            'Exceeding the word limit (e.g. writing "the renewable energy" instead of "renewable energy").',
            "Paraphrasing instead of copying exact words.",
            "Missing the answer because the question uses a synonym, not the passage's exact phrase.",
        ],
        "confusing": (
            "The question sentence is usually a paraphrase of the passage sentence — so you need "
            "to spot the paraphrase to find where the answer is, then copy the original word from "
            "the passage, not the paraphrase."
        ),
    },
    {
        "title": "Short answer",
        "badges": [("Core", "core"), ("Gap", "gap")],
        "how": (
            "Answer questions in your own words using information from the passage. Strict word "
            "limit applies. Answers are usually nouns or noun phrases found directly in the text."
        ),
        "focus": "Scanning for precise factual details",
        "mistakes": [
            "Writing full sentences instead of short answers.",
            "Exceeding the word limit.",
            "Copying too much from the passage — just give the key noun or phrase.",
        ],
        "confusing": (
            "Test takers often write a full explanation when one or two words from the passage "
            "is the complete answer."
        ),
    },
    {
        "title": "Summary completion (box)",
        "badges": [("Gap", "gap"), ("Core", "core")],
        "how": (
            "A summary of part of the passage is given with gaps. A box of words is provided. "
            "You choose the correct word from the box to fill each gap. Words in the box include "
            "distractors that fit grammatically but mean something different."
        ),
        "focus": "Understanding meaning in context and eliminating distractors",
        "mistakes": [
            "Choosing a word that fits grammatically but changes the meaning.",
            "Not returning to the passage to verify.",
            "Using a word that sounds related to the topic but is not the correct meaning.",
        ],
        "confusing": (
            "All words in the box will seem plausible — they are designed to. Always go back "
            "to the passage and check meaning in context, not just grammatical fit."
        ),
    },
]


@login_required
def strategies(request):
    return render(
        request,
        "reading/strategies.html",
        {
            "streak": get_streak(request.user),
            "question_types": READING_QUESTION_TYPES,
            **_streak_ctx(request),
        },
    )


@login_required
def skills(request):
    return render(
        request,
        "reading/skills.html",
        {
            "streak": get_streak(request.user),
            **_streak_ctx(request),
        },
    )


GENERAL_READING_SEED = [
    {
        "slug": "cities-cleaner-air",
        "title": "How cities are redesigning streets for cleaner air",
        "description": "Urban planners are replacing car lanes with green corridors — the results are measurable.",
        "topic": "environment",
        "level": "intermediate",
        "minutes": 5,
        "words": 320,
        "question_count": 5,
        "is_featured": True,
        "paragraphs": [
            "Urban planners in many capitals are redesigning streets because transport data shows a mismatch between how roads were built and how people now move. In most inner districts, a large share of trips are short and can be walked, cycled, or completed by bus, yet road space still favors private cars. City teams are reallocating one lane at a time into protected cycle tracks, wider pavements, and shaded waiting areas for public transport. The aim is not to ban cars completely, but to make cleaner options safe, predictable, and attractive enough that people choose them without needing constant enforcement.",
            "Early pilots near schools and hospitals show why this approach matters for health outcomes. When through-traffic is redirected and junction timing is changed, air quality sensors often record a measurable drop in peak pollution around the most sensitive sites. Parents report that walking routes feel safer, and bus operators record more stable travel times because fewer vehicles block priority lanes. In several cities, local shops initially worried about reduced parking, but footfall recovered once streets became easier to cross and outdoor seating increased. Those shifts suggest that cleaner-air planning can support both mobility and local commerce when the design sequence is carefully managed.",
            "Implementation, however, is where many projects fail. If freight windows are unclear, delivery vehicles can create new bottlenecks that frustrate residents and businesses. If cycle lanes stop suddenly at dangerous intersections, users lose trust in the network. And if planners communicate only final designs without explaining trial phases, communities may interpret temporary disruption as permanent decline. Successful programs therefore use staged rollouts, publish baseline traffic and pollution data, and adjust quickly after feedback. This transparent process helps separate short-term inconvenience from long-term benefits and gives policymakers evidence to defend difficult trade-offs.",
            "For IELTS learners, this topic is useful because it naturally supports high-scoring argument structure. You can present a claim, support it with measurable evidence, acknowledge a limitation, and then propose a practical solution. Useful collocations include improve air quality, redesign urban corridors, manage implementation risk, and balance mobility priorities. In Writing Task 2, this language helps you sound precise rather than generic. In Speaking Part 3, it also helps you discuss policy realistically by showing that urban change is neither simple nor impossible, but dependent on sequencing, communication, and accountability.",
        ],
        "vocab": [
            {"word": "reallocating", "pron": "/ˌriːˈæləkeɪtɪŋ/", "def": "distributing resources in a different way"},
            {"word": "corridors", "pron": "/ˈkɒrɪdɔːz/", "def": "routes or channels used for movement"},
            {"word": "congestion", "pron": "/kənˈdʒestʃən/", "def": "too much traffic causing delay"},
            {"word": "emissions", "pron": "/ɪˈmɪʃənz/", "def": "polluting gases released into the air"},
            {"word": "predictable", "pron": "/prɪˈdɪktəbəl/", "def": "happening in a consistent way"},
            {"word": "limitation", "pron": "/ˌlɪmɪˈteɪʃən/", "def": "a restriction or weakness"},
        ],
        "questions_json": [
            {"q": "What was reallocated in pilot zones?", "options": ["School budgets", "Street space", "Hospital beds", "River water"], "answer": 1, "exp": "Paragraph 1 states street space was reallocated."},
            {"q": "Which outcome happened near schools?", "options": ["More traffic fines", "Lower emissions", "Higher parking demand", "Fewer buses"], "answer": 1, "exp": "Paragraph 2 reports emissions dropped near schools."},
            {"q": "What can reduce trust in redesign plans?", "options": ["Fast buses", "Clear freight windows", "Weak alternatives", "More cycle lanes"], "answer": 2, "exp": "Paragraph 3 warns failure happens when alternatives are weak."},
            {"q": "What writing structure does the text highlight?", "options": ["Narrative only", "Cause-evidence-limitation", "Dialogue format", "Chronological biography"], "answer": 1, "exp": "Paragraph 4 explicitly names cause, evidence, and limitation."},
            {"q": "The main topic is best described as:", "options": ["Airport expansion", "Street redesign for cleaner mobility", "University admissions", "Hospital staffing"], "answer": 1, "exp": "All paragraphs center on urban street redesign and outcomes."},
        ],
    },
    {
        "slug": "sleep-memory",
        "title": "Why sleep deprivation affects memory",
        "description": "Short sleep cycles reduce memory consolidation.",
        "topic": "health",
        "level": "beginner",
        "minutes": 4,
        "words": 240,
        "question_count": 5,
        "paragraphs": [
            "Sleep is not passive downtime for the brain; it is an active biological process that helps organise, stabilise, and prioritize information gathered during the day. During different sleep stages, newly learned material is replayed and integrated with older knowledge, making recall faster and more accurate later. This is especially important for language learners who need to retain vocabulary, collocations, and grammar patterns across multiple contexts. Without enough sleep, learners may still recognize familiar terms, but they struggle to retrieve them quickly under test conditions where timing and clarity matter.",
            "When sleep duration drops repeatedly, attention control and working memory usually decline first. That means students can read a passage and think they understood it, yet miss key connectors, qualifiers, or contrast markers that determine the correct answer. In listening tasks, short lapses of concentration lead to lost details that cannot be recovered. In writing tasks, fatigue increases the chance of repetition and weak word choice because the brain defaults to high-frequency language. Over time, this pattern creates the impression that a learner has plateaued, when the real issue may be recovery quality rather than study effort.",
            "Evidence from school and university settings consistently shows that students with stable sleep schedules perform better on comprehension, recall, and complex problem-solving than peers who rely on last-minute cramming. The difference is not only total hours but also regularity. Going to bed and waking up at roughly the same time helps the body maintain stronger circadian rhythms, which improves alertness during daytime study sessions. Regularity also reduces decision fatigue: when rest is predictable, learners can maintain a routine for review, reading practice, and speaking drills instead of cycling between overwork and exhaustion.",
            "For IELTS preparation, the practical lesson is simple: build sleep into your strategy as a performance tool, not a reward after studying. Keep revision blocks short, finish intense work at least an hour before bedtime, and review difficult vocabulary again the next morning to strengthen recall pathways. This approach creates active memory rather than passive recognition, which is exactly what high-band responses require. In essays and speaking answers, you can discuss this topic using precise phrases such as memory consolidation, cognitive overload, and long-term retention to demonstrate lexical control.",
        ],
        "vocab": [
            {"word": "deprivation", "pron": "/ˌdeprɪˈveɪʃən/", "def": "not having enough of something essential"},
            {"word": "consolidation", "pron": "/kənˌsɒlɪˈdeɪʃən/", "def": "strengthening memory over time"},
            {"word": "recall", "pron": "/rɪˈkɔːl/", "def": "to remember information"},
            {"word": "reliable", "pron": "/rɪˈlaɪəbəl/", "def": "consistently dependable"},
            {"word": "comprehension", "pron": "/ˌkɒmprɪˈhenʃən/", "def": "understanding of text"},
            {"word": "consistent", "pron": "/kənˈsɪstənt/", "def": "regular and steady"},
        ],
        "questions_json": [
            {"q": "Sleep mainly helps the brain to:", "options": ["Grow muscles", "Organise information", "Boost appetite", "Reduce vocabulary"], "answer": 1, "exp": "Paragraph 1 says sleep helps organise information."},
            {"q": "When sleep is reduced, recall becomes:", "options": ["More reliable", "Less reliable", "Unchanged", "Instant"], "answer": 1, "exp": "Paragraph 2 says recall becomes less reliable."},
            {"q": "Who performed better?", "options": ["People with enough sleep", "People with no sleep", "Only teachers", "None"], "answer": 0, "exp": "Paragraph 3 says students with enough sleep did better."},
            {"q": "What beats cramming?", "options": ["Coffee", "Consistent sleep", "Longer classes", "No breaks"], "answer": 1, "exp": "Paragraph 4 gives consistent sleep as better than cramming."},
            {"q": "Main message:", "options": ["Skip sleep to study", "Sleep quality supports memory", "Memory is random", "Only diet matters"], "answer": 1, "exp": "All paragraphs connect sleep with memory outcomes."},
        ],
    },
    {
        "slug": "ai-hidden-cost",
        "title": "The hidden cost of artificial intelligence",
        "description": "Data-centre growth changes energy demand and infrastructure planning.",
        "topic": "technology",
        "level": "advanced",
        "minutes": 7,
        "words": 480,
        "question_count": 5,
        "paragraphs": [
            "Artificial intelligence is often discussed as a software revolution, yet its physical footprint is increasingly visible in electricity demand, cooling systems, and grid planning. As models become larger and services attract more daily users, compute needs expand not only during model training but also during continuous inference. In practical terms, every query requires processing power, and small latency improvements often require additional hardware. This means product success can increase energy use faster than expected, especially when services are global and available at all hours. The hidden cost is therefore not a single expense, but a persistent infrastructure commitment.",
            "Data-centre operators now negotiate long-term power agreements and upgrade backup systems because demand variability can be extreme. Facilities that once supported predictable enterprise workloads must now handle bursts from consumer-facing AI tools, often with stricter uptime expectations. Cooling is another pressure point: as chip density rises, thermal management becomes both expensive and water-intensive in some regions. Local utilities, meanwhile, face difficult decisions about grid reinforcement timelines and allocation priorities. When multiple projects seek connection in the same area, permitting can slow and developers may face delays that directly affect product launch schedules.",
            "Regulators and investors have responded by asking for clearer disclosures rather than broad sustainability claims. They want comparable metrics on power consumption per workload, source of electricity, and assumptions behind efficiency projections. Without standardized reporting, it is difficult to evaluate whether a company has genuinely improved performance or simply shifted costs elsewhere in the stack. This transparency debate is likely to intensify as governments connect digital growth targets with climate commitments. Firms that cannot explain their resource profile in concrete terms may face reputational risk, financing friction, or stricter compliance requirements over time.",
            "Efficiency still provides a real path forward, but it is not automatic. Better model architectures, quantization, and workload routing can reduce cost per request, while modern chips can deliver more output per watt. However, rebound effects are common: when systems become cheaper and faster, usage rises, and total demand can continue climbing. Strategic planning therefore requires both innovation and governance. For IELTS candidates, this topic supports nuanced writing because it allows balanced argumentation: AI can create value, yet responsible scaling depends on transparent metrics, infrastructure foresight, and policy coordination.",
        ],
        "vocab": [],
        "questions_json": [],
    },
    {
        "slug": "remote-work-centres",
        "title": "How remote work changed city centres",
        "description": "Commuting and retail footfall shifted rapidly across business districts.",
        "topic": "society",
        "level": "intermediate",
        "minutes": 5,
        "words": 300,
        "question_count": 5,
        "paragraphs": [
            "Remote work changed city centres by weakening the old pattern of five identical commuting days. Before hybrid schedules became common, transport systems and business districts were designed around predictable morning and evening peaks. Now attendance varies by company policy, team role, and project cycle, so demand is less stable and harder to forecast. Office towers may be nearly full on Tuesday and Wednesday but far quieter on Monday and Friday. This uneven rhythm affects everything from train frequency decisions to coffee shop staffing, because businesses can no longer rely on one steady weekday customer flow.",
            "Spending patterns shifted alongside commuting habits. Retailers in central districts report stronger lunchtime trade on high-attendance days, but weaker baseline sales across the week. Restaurants and service providers have adapted by concentrating promotions, changing opening hours, and reducing fixed labor costs where possible. Some areas have successfully diversified by attracting leisure activity, events, or education services that are not tied to office occupancy. Others still struggle because their local economy depended heavily on daily office workers. The key lesson is that footfall has not disappeared entirely; it has become more selective in timing and purpose.",
            "Commercial property markets have also adjusted. Tenants increasingly request flexible layouts, shorter lease terms, and buildings with stronger amenities that justify commuting. Landlords now compete on experience as much as location, offering better ventilation, collaboration space, and shared services. At the same time, municipal planners must reconsider assumptions used in transport modeling, public safety coverage, and street maintenance budgets. If peak-hour pressure is lower but spread across different times, systems designed for one intense rush period may no longer be efficient. This creates a planning challenge that is operational, financial, and social at the same time.",
            "Cities responding well to this transition usually adopt mixed-use strategies. They encourage residential conversion in underused office zones, support small business adaptation, and redesign public space to keep districts active beyond standard work hours. Transport agencies are experimenting with more dynamic scheduling and clearer real-time information to match variable demand. For IELTS writing, this topic helps you demonstrate cause-and-effect reasoning with balanced evaluation: remote work reduces certain pressures, but it also introduces new complexity. Strong responses acknowledge both opportunity and disruption, then propose realistic policy measures rather than absolute predictions.",
        ],
        "vocab": [],
        "questions_json": [],
    },
    {
        "slug": "spaced-repetition",
        "title": "Why spaced repetition beats cramming",
        "description": "Smaller review sessions over weeks improve long-term retention.",
        "topic": "education",
        "level": "beginner",
        "minutes": 4,
        "words": 220,
        "question_count": 5,
        "paragraphs": [
            "Spaced repetition outperforms cramming because memory improves when retrieval is timed, effortful, and repeated across intervals. When learners review a word right before they are likely to forget it, recall requires more cognitive work, and that effort strengthens the memory trace. Over multiple cycles, retrieval becomes faster and more reliable in different contexts. This is exactly what language exams demand: not just recognition on a list, but flexible access while reading complex texts, planning essays, or responding in real-time speaking tasks. The method works because it aligns revision with how memory naturally decays and rebuilds.",
            "Cramming can still produce temporary gains, which is why many students trust it. After a long review session, vocabulary feels familiar and confidence rises. However, that feeling often reflects short-term fluency rather than durable learning. Within days, much of the material fades, especially low-frequency words that were not reused in authentic contexts. Under timed conditions, learners then default to basic vocabulary because advanced terms are not available quickly enough. This gap between perceived and actual mastery is one reason students feel frustrated: they study hard, but the structure of revision does not support long-term retrieval.",
            "Distributed sessions are also better for attention management. Short focused reviews reduce fatigue and make error patterns easier to detect. If a learner repeatedly confuses similar words, the system can surface that weakness and schedule targeted practice instead of forcing another full-list review. This adaptive cycle saves time and lowers stress because progress is visible and specific. In contrast, marathon sessions mix easy and difficult items without clear prioritization, so effort is often spent where it is least needed. Spaced systems direct effort toward weak items, which increases efficiency over weeks rather than hours.",
            "For IELTS candidates, the practical model is simple: learn new words with context, review the next day, then again after three days, then after a week, and continue widening intervals as recall improves. Pair each review with short production tasks such as writing one sentence or speaking one example aloud. That turns passive recognition into active vocabulary, which examiners reward in both writing and speaking. Useful terms for high-band responses include retention curve, active recall, and lexical flexibility. These phrases help you explain not only what strategy works, but why it works.",
        ],
        "vocab": [],
        "questions_json": [],
    },
    {
        "slug": "delayed-climate-targets",
        "title": "When companies delay climate targets",
        "description": "Investors react when long-term promises miss interim milestones.",
        "topic": "business",
        "level": "intermediate",
        "minutes": 5,
        "words": 300,
        "question_count": 5,
        "paragraphs": [
            "Companies increasingly publish long-term climate targets, but markets now pay closer attention to interim milestones than final dates alone. A pledge for 2040 or 2050 sounds ambitious, yet investors need near-term indicators to evaluate execution risk. Without annual benchmarks, it is difficult to distinguish credible transition plans from aspirational messaging. Analysts therefore track measurable items such as emissions intensity, capital expenditure allocation, supplier standards, and energy sourcing changes. These indicators reveal whether strategy is moving from presentation slides into operational decisions, which is where financial implications become visible.",
            "When milestones are delayed, market response depends less on the delay itself and more on the quality of explanation. If firms provide specific evidence about technology constraints, permitting delays, or supply bottlenecks, investors may treat revised timelines as manageable. If explanations are vague, shifting, or inconsistent across reports, credibility erodes quickly. The issue is not only environmental reputation; it is governance quality. Stakeholders interpret unclear communication as a signal that leadership lacks control over execution assumptions. In sectors with high regulatory exposure, that perception can raise financing costs and reduce strategic flexibility.",
            "Capital reallocation can happen rapidly when comparable alternatives exist. Funds may rotate toward competitors that show clearer progress metrics, stronger disclosure discipline, or better alignment between incentives and transition goals. Credit markets can respond similarly if lenders perceive widening risk around compliance penalties or stranded assets. This dynamic creates pressure on firms to improve not just performance, but comparability. Standardized baselines, transparent methodology, and independent verification help investors assess progress consistently across reporting periods. Without those elements, even genuine progress can be discounted because external audiences cannot confirm its scale or durability.",
            "For IELTS writing, this topic offers a strong framework for balanced analysis. You can argue that ambitious targets matter, but credibility depends on interim delivery and transparent governance. Effective vocabulary includes interim milestones, disclosure quality, execution risk, and investor confidence. In Task 2 essays, avoid absolute claims such as all delays are failure; instead, show nuance by distinguishing justified revisions from weak accountability. This approach demonstrates mature reasoning and supports higher coherence scores because each paragraph connects cause, interpretation, and consequence in a logical sequence.",
        ],
        "vocab": [],
        "questions_json": [],
    },
    {
        "slug": "microplastics-bloodstream",
        "title": "Microplastics found in human bloodstream",
        "description": "Researchers debate how concentration relates to long-term risk.",
        "topic": "science",
        "level": "intermediate",
        "minutes": 5,
        "words": 310,
        "question_count": 5,
        "paragraphs": [
            "Microplastics have been detected in human blood samples in several recent studies, increasing concern about how widely synthetic particles circulate through environmental and biological systems. Potential exposure routes include drinking water, food packaging, household dust, and airborne fibers in dense urban settings. Detection does not automatically confirm harm, but it does establish that particles can pass barriers once assumed to be protective. This finding shifts the debate from whether exposure exists to how concentration, particle type, and long-term accumulation may influence health outcomes over time.",
            "Researchers emphasize that method quality is crucial when interpreting results. Sampling protocols, contamination controls, and analytical techniques still vary across laboratories, and these differences can affect reported concentration levels. For example, tiny fibers from clothing or lab equipment can contaminate samples if handling standards are inconsistent. Because of this, cross-study comparisons require caution unless methods are clearly documented and reproducible. The strongest papers now include blank controls, material tracking, and detailed reporting on detection thresholds to reduce uncertainty and improve confidence in findings.",
            "At present, evidence linking specific concentration levels to direct clinical outcomes remains limited, so public communication should avoid sensational claims. Most experts frame current findings as an early warning rather than final proof of causation. That distinction matters for policy: overstatement can damage trust, while understatement can delay preventive action. A balanced approach supports continued monitoring, targeted toxicology research, and stronger source reduction strategies in high-exposure environments. This keeps policy proportional to current evidence while still acknowledging the potential scale of long-term risk.",
            "From an IELTS perspective, this is an ideal science-and-society topic because it requires precise language and careful qualification. Strong lexical choices include exposure pathways, measurement uncertainty, precautionary policy, and evidence threshold. In writing tasks, high-band responses usually avoid binary conclusions and instead evaluate what is known, what is uncertain, and what actions remain reasonable under uncertainty. This structure shows critical thinking and coherence while allowing you to integrate scientific caution with practical policy recommendations.",
        ],
        "vocab": [],
        "questions_json": [],
    },
]


def _ensure_general_reading_seed():
    for i, row in enumerate(GENERAL_READING_SEED):
        payload = dict(row)
        paragraphs = payload.get("paragraphs") or []
        if paragraphs:
            payload["words"] = sum(
                len(re.findall(r"[A-Za-z0-9']+", paragraph)) for paragraph in paragraphs
            )
        payload.setdefault("is_featured", i == 0)
        payload.setdefault("is_active", True)
        GeneralReadingArticle.objects.update_or_create(
            slug=payload["slug"], defaults=payload
        )


def _serialize_general_article(article: GeneralReadingArticle):
    paragraphs = article.paragraphs or []
    calculated_words = sum(
        len(re.findall(r"[A-Za-z0-9']+", paragraph)) for paragraph in paragraphs
    )
    return {
        "id": article.slug,
        "slug": article.slug,
        "title": article.title,
        "desc": article.description,
        "description": article.description,
        "topic": article.topic,
        "level": article.level,
        "minutes": article.minutes,
        "words": calculated_words or article.words,
        "questions": article.question_count,
        "paragraphs": paragraphs,
        "vocab": article.vocab or [],
        "questionsData": article.questions_json or [],
        "isFeatured": article.is_featured,
    }


@login_required
def general_reading(request):
    _ensure_general_reading_seed()
    articles = list(GeneralReadingArticle.objects.filter(is_active=True).order_by("-is_featured", "title"))
    article_payload = [_serialize_general_article(a) for a in articles]

    sessions = list(
        GeneralReadingSession.objects.filter(student=request.user).select_related("article")[:50]
    )
    bookmarks = list(
        GeneralReadingBookmark.objects.filter(student=request.user).values_list(
            "article__slug", flat=True
        )
    )
    summaries = list(
        GeneralReadingSummary.objects.filter(student=request.user)
        .select_related("article")
        .order_by("-updated_at")[:5]
    )

    bootstrap = {
        "articles": article_payload,
        "bookmarks": bookmarks,
        "history": [
            {
                "date": s.created_at.date().isoformat(),
                "articleSlug": s.article.slug,
                "title": s.article.title,
                "topic": s.article.topic,
                "score": s.score,
                "total": s.total_questions,
                "wpm": s.wpm,
                "timeSecs": s.time_taken_secs,
            }
            for s in sessions
        ],
        "completedToday": [
            {
                "title": s.article.title,
                "topic": s.article.topic,
                "score": s.score,
                "total": s.total_questions,
                "wpm": s.wpm,
                "date": s.created_at.date().isoformat(),
            }
            for s in sessions
            if s.created_at.date() == timezone.localdate()
        ],
        "lastSummary": {
            "text": summaries[0].summary_text if summaries else "",
            "articleSlug": summaries[0].article.slug if summaries and summaries[0].article else "",
            "date": summaries[0].updated_at.date().isoformat() if summaries else "",
        },
        "speedSessions": [
            {
                "date": s.created_at.date().isoformat(),
                "articleSlug": s.article.slug,
                "wpm": s.wpm,
            }
            for s in sessions[:30]
        ],
        "streak": get_streak(request.user),
    }
    return render(
        request,
        "reading/general_reading.html",
        {
            "streak": get_streak(request.user),
            "general_reading_bootstrap": bootstrap,
            **_streak_ctx(request),
        },
    )


@login_required
@require_POST
def general_log_session(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    slug = (payload.get("article_slug") or "").strip()
    score = int(payload.get("score") or 0)
    total = int(payload.get("total_questions") or 5)
    wpm = int(payload.get("wpm") or 0)
    time_taken = int(payload.get("time_taken_secs") or 0)
    if not slug:
        return JsonResponse({"ok": False, "error": "missing_article_slug"}, status=400)

    article = GeneralReadingArticle.objects.filter(slug=slug, is_active=True).first()
    if not article:
        return JsonResponse({"ok": False, "error": "article_not_found"}, status=404)

    sess = GeneralReadingSession.objects.create(
        student=request.user,
        article=article,
        score=score,
        total_questions=total or 5,
        correct_answers=score,
        wpm=wpm,
        time_taken_secs=time_taken,
    )
    ReadingAttempt.objects.create(
        student=request.user,
        test_type="general",
        score=float(score),
        total_questions=total or 5,
        correct_answers=score,
        time_taken_secs=time_taken,
        completed=True,
    )
    return JsonResponse({"ok": True, "session_id": sess.pk})


@login_required
@require_POST
def general_toggle_bookmark(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)
    slug = (payload.get("article_slug") or "").strip()
    if not slug:
        return JsonResponse({"ok": False, "error": "missing_article_slug"}, status=400)
    article = GeneralReadingArticle.objects.filter(slug=slug, is_active=True).first()
    if not article:
        return JsonResponse({"ok": False, "error": "article_not_found"}, status=404)

    row = GeneralReadingBookmark.objects.filter(student=request.user, article=article).first()
    if row:
        row.delete()
        return JsonResponse({"ok": True, "bookmarked": False})
    GeneralReadingBookmark.objects.create(student=request.user, article=article)
    return JsonResponse({"ok": True, "bookmarked": True})


@login_required
@require_POST
def general_summary_feedback(request):
    """Analyse user's reading summary with Anthropic; always returns JSON."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    article_title = (payload.get("article_title") or "").strip()
    article_text = (payload.get("article_text") or "").strip()
    summary = (payload.get("summary") or "").strip()
    article_slug = (payload.get("article_slug") or "").strip()
    if not article_text or not summary:
        return JsonResponse({"ok": False, "error": "missing_fields"}, status=400)

    article_obj = None
    if article_slug:
        article_obj = GeneralReadingArticle.objects.filter(slug=article_slug).first()

    api_key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
    if not api_key:
        GeneralReadingSummary.objects.create(
            student=request.user,
            article=article_obj,
            summary_text=summary,
            feedback_json={},
        )
        return JsonResponse(
            {
                "ok": False,
                "error": "anthropic_key_missing",
                "message": "Could not analyse right now — summary saved anyway.",
            },
            status=503,
        )

    prompt = (
        "You are an IELTS reading coach. Compare the student's summary with the article.\n"
        "Return ONLY JSON with these keys:\n"
        "accuracy_label (green|amber|red), score (0-5 integer), got_right, missed, "
        "model_summary, tip.\n\n"
        f"ARTICLE TITLE:\n{article_title}\n\n"
        f"ARTICLE TEXT:\n{article_text}\n\n"
        f"STUDENT SUMMARY:\n{summary}\n"
    )
    req_body = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 600,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(req_body).encode("utf-8"),
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read().decode("utf-8")
        ai = json.loads(raw)
        content = ai.get("content") or []
        text = ""
        if content and isinstance(content, list):
            text = (content[0].get("text") or "").strip()
        parsed = json.loads(text)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError):
        GeneralReadingSummary.objects.create(
            student=request.user,
            article=article_obj,
            summary_text=summary,
            feedback_json={},
        )
        return JsonResponse(
            {
                "ok": False,
                "error": "analysis_failed",
                "message": "Could not analyse right now — summary saved anyway.",
            },
            status=503,
        )

    score = parsed.get("score", 0)
    try:
        score = max(0, min(5, int(score)))
    except (TypeError, ValueError):
        score = 0

    label = (parsed.get("accuracy_label") or "").strip().lower()
    if label not in {"green", "amber", "red"}:
        if score >= 4:
            label = "green"
        elif score >= 2:
            label = "amber"
        else:
            label = "red"

    feedback_payload = {
        "accuracy_label": label,
        "score": score,
        "got_right": (parsed.get("got_right") or "").strip(),
        "missed": (parsed.get("missed") or "").strip(),
        "model_summary": (parsed.get("model_summary") or "").strip(),
        "tip": (parsed.get("tip") or "").strip(),
    }
    GeneralReadingSummary.objects.create(
        student=request.user,
        article=article_obj,
        summary_text=summary,
        feedback_json=feedback_payload,
    )
    return JsonResponse({"ok": True, "feedback": feedback_payload})


@login_required
def academic_tests_index(request):
    tests = ReadingTest.objects.order_by("number")
    academic_results = (
        ReadingTestResult.objects.filter(user=request.user, test__slug="academic-1")
        .select_related("test")
        .order_by("-completed_at")
    )
    attempt_count = academic_results.count()
    recent_attempts = academic_results[:25]
    best_row = academic_results.order_by("-score", "-completed_at").first()
    best_score = best_row.score if best_row else None
    best_result_id = best_row.pk if best_row else None
    best_band = best_row.band if best_row else None
    last_row = academic_results.first()
    return render(
        request,
        "reading/academic_tests_list.html",
        {
            "tests": tests,
            "academic_attempt_count": attempt_count,
            "academic_recent_attempts": recent_attempts,
            "academic_best_score": best_score,
            "academic_best_result_id": best_result_id,
            "academic_best_band": best_band,
            "academic_last_score": last_row.score if last_row else None,
            "academic_last_band": last_row.band if last_row else None,
            **_streak_ctx(request),
        },
    )


@login_required
def academic_test_session(request, test_number: int):
    if test_number != 1:
        raise Http404("Test not available")
    test = get_object_or_404(ReadingTest, number=test_number, is_live=True)
    return render(
        request,
        "reading/academic_test_session.html",
        {
            "test": test,
            "test_payload": get_client_test_payload(),
            "submit_url": reverse("reading:academic_test_submit", kwargs={"test_number": test_number}),
            "tests_index_url": reverse("reading:academic_tests_index"),
        },
    )


@login_required
@require_POST
def academic_test_submit(request, test_number: int):
    if test_number != 1:
        return JsonResponse({"ok": False, "error": "not_found"}, status=404)
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "bad_json"}, status=400)
    raw_answers = body.get("answers") or {}
    if not isinstance(raw_answers, dict):
        raw_answers = {}
    answers = {str(k): str(v) for k, v in raw_answers.items()}
    try:
        time_taken = int(body.get("time_taken_seconds") or 0)
    except (TypeError, ValueError):
        time_taken = 0
    time_taken = max(0, min(time_taken, 3600))
    score, p1, p2, p3 = score_answers(answers)
    band = band_from_score(score)
    test = get_object_or_404(ReadingTest, number=test_number, is_live=True)
    ReadingTestResult.objects.create(
        user=request.user,
        test=test,
        score=score,
        band=band,
        time_taken_seconds=time_taken,
        part1_score=p1,
        part2_score=p2,
        part3_score=p3,
    )
    return JsonResponse(
        {
            "ok": True,
            "score": score,
            "band": band,
            "time_taken_seconds": time_taken,
            "part1_score": p1,
            "part2_score": p2,
            "part3_score": p3,
            "part1_max": 14,
            "part2_max": 13,
            "part3_max": 13,
        }
    )
