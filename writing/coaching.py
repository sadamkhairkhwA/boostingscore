"""AI coaching for IELTS writing (3-draft flow) and paraphrase practice."""
from __future__ import annotations

import re
from typing import Any

from .feedback_levels import feedback_language_instruction
from .grading import fetch_openai_json_messages
from .models import WritingQuestion
from .span_schema import (
    SPAN_JSON_RULES_COACH,
    SPAN_JSON_RULES_PARAPHRASE,
    normalize_span_list,
)

PARAPHRASE_SYSTEM = """You are an expert English teacher helping learners improve their writing.
The student is doing a paraphrase exercise. Return JSON only (no markdown fences) with exactly these keys:
- reference_improved_version: a polished rewrite of their text (string), same approximate length and meaning
- collocations: string — suggest 2–4 stronger collocations or chunks they could use (with brief examples)
- grammar_notes: string — 2–4 clear grammar points to fix or learn (mini-lesson tone)
- vocabulary_upgrades: string — weaker words/phrases → stronger academic alternatives
- what_to_improve: string — short summary of priorities (bullet-style in one string is OK)
""" + SPAN_JSON_RULES_PARAPHRASE + """
Be specific and quote short fragments from their text where helpful. Encouraging tone."""

GENERATE_PARAPHRASE_PROMPT = """You write short original English texts for language learners (paraphrase practice).
Return JSON only: {"source_text": "..."}.
The source_text must be your own neutral informative prose on the topic — not exam instructions, not bullet lists.
Length by level:
- Level 1: 2–4 short simple sentences, about 35–55 words total, everyday vocabulary (A2–B1).
- Level 2: one paragraph, 52–68 words, B1 level.
- Level 3: one paragraph, 75–115 words, B1–B2 level.
No title line; no "The graph shows" unless the topic is clearly about data — prefer general topic sentences the student can rephrase freely."""

COACH_ROUND1_TASK1 = """You coach IELTS Academic Task 1 writing. The student just wrote a FIRST draft (not final).
Return JSON only with keys:
- deficiencies: string — main problems (data description, overview, comparison, tense, etc.)
- grammar_to_study: string — focused mini-lesson on 1–2 grammar patterns they should master for Task 1
- vocabulary_and_collocations: string — words/collocations to upgrade for describing data
- rewrite_focus: string — exactly what they should try to improve in their next full rewrite (draft 2)
""" + SPAN_JSON_RULES_COACH + """
Be concrete and teach; do not give band scores yet. issue_spans and strength_spans refer to DRAFT 1 only."""

COACH_ROUND1_TASK2 = """You coach IELTS Task 2 essay writing. The student just wrote a FIRST draft.
Return JSON only with keys:
- deficiencies: string — argument, task response, structure, development issues
- grammar_to_study: string — mini-lesson on grammar patterns relevant to their mistakes
- vocabulary_and_collocations: string — academic vocabulary and collocations to use
- rewrite_focus: string — what to improve in draft 2
""" + SPAN_JSON_RULES_COACH + """
Teach clearly; no band scores yet. issue_spans and strength_spans refer to DRAFT 1 only."""

COACH_ROUND2 = """You are an IELTS writing coach. The student wrote DRAFT 1, received feedback, then wrote DRAFT 2 for the same question.
Task type is either Task 1 (Academic) or Task 2 — you are told which in the user message.
Return JSON only with keys:
- improvements_since_draft1: string — what got better and what is still weak
- topic_and_task_response: string — how well they address the question / data now
- ielts_tips_for_this_question_type: string — 3–5 practical tips for THIS task type (Task 1 or Task 2) and this prompt style
- short_roadmap: string — 4–6 step study roadmap for the next week (bullets in one string)
- rewrite_focus: string — what to polish in draft 3 (final practice version)
""" + SPAN_JSON_RULES_COACH + """
Encouraging but honest. issue_spans and strength_spans refer to DRAFT 2 only."""

COACH_ROUND3 = """You are an IELTS writing coach. The student completed THREE drafts for one question. Official-style scores were assigned to draft 3 (provided in the user message).
Return JSON only with keys:
- journey_summary: string — how draft 1 → 2 → 3 evolved
- final_study_points: string — top grammar and vocabulary priorities going forward
- exam_day_reminders: string — short checklist for IELTS writing on test day
""" + SPAN_JSON_RULES_COACH + """
Do not repeat full band scores; reference them briefly only if useful. issue_spans and strength_spans refer to DRAFT 3 only."""


def _task_label(qtype: str) -> str:
    return "IELTS Academic Task 1" if qtype == WritingQuestion.TASK1 else "IELTS Task 2"


def _with_spans(d: dict[str, Any]) -> dict[str, Any]:
    out = dict(d)
    out["issue_spans"] = normalize_span_list(out.get("issue_spans"))
    out["strength_spans"] = normalize_span_list(out.get("strength_spans"))
    return out


def generate_paraphrase_source(*, topic_label: str, topic_code: str, level: int) -> str:
    user = (
        f"Topic theme for the paragraph: {topic_label} (internal code: {topic_code}).\n"
        f"Practice level number: {level} (see length rules in your instructions).\n"
        "Write one source_text only."
    )
    parsed = fetch_openai_json_messages(
        messages=[
            {"role": "system", "content": GENERATE_PARAPHRASE_PROMPT},
            {"role": "user", "content": user},
        ],
        temperature=0.75,
        max_completion_tokens=1024,
    )
    text = str(parsed.get("source_text") or "").strip()
    if len(text) < 20:
        raise RuntimeError("Model returned empty or very short source text.")
    return text


def coach_round_one(
    *,
    question_text: str,
    question_type: str,
    draft_text: str,
    word_count: int,
    learner_level: int = 3,
) -> dict[str, Any]:
    base = COACH_ROUND1_TASK1 if question_type == WritingQuestion.TASK1 else COACH_ROUND1_TASK2
    system = base + feedback_language_instruction(learner_level)
    user = (
        f"{_task_label(question_type)}.\n\n"
        f"Question:\n{question_text}\n\n"
        f"DRAFT 1 ({word_count} words):\n{draft_text}\n"
    )
    return _with_spans(
        fetch_openai_json_messages(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.4,
            max_completion_tokens=3072,
        )
    )


def coach_round_two(
    *,
    question_text: str,
    question_type: str,
    draft_1: str,
    draft_2: str,
    wc1: int,
    wc2: int,
    round_1_feedback: dict[str, Any],
    learner_level: int = 3,
) -> dict[str, Any]:
    system = COACH_ROUND2 + feedback_language_instruction(learner_level)
    user = (
        f"Task: {_task_label(question_type)}.\n\n"
        f"Question:\n{question_text}\n\n"
        f"Round 1 coach notes (JSON summary for you):\n{round_1_feedback}\n\n"
        f"DRAFT 1 ({wc1} words):\n{draft_1}\n\n"
        f"DRAFT 2 ({wc2} words):\n{draft_2}\n"
    )
    return _with_spans(
        fetch_openai_json_messages(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.4,
            max_completion_tokens=3072,
        )
    )


def coach_round_three(
    *,
    question_text: str,
    question_type: str,
    draft_1: str,
    draft_2: str,
    draft_3: str,
    wc1: int,
    wc2: int,
    wc3: int,
    grading_summary: str,
    learner_level: int = 3,
) -> dict[str, Any]:
    system = COACH_ROUND3 + feedback_language_instruction(learner_level)
    user = (
        f"{_task_label(question_type)}.\n\n"
        f"Question:\n{question_text}\n\n"
        f"Grading summary for DRAFT 3:\n{grading_summary}\n\n"
        f"DRAFT 1 ({wc1} words):\n{draft_1}\n\n"
        f"DRAFT 2 ({wc2} words):\n{draft_2}\n\n"
        f"DRAFT 3 ({wc3} words):\n{draft_3}\n"
    )
    return _with_spans(
        fetch_openai_json_messages(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.35,
            max_completion_tokens=2048,
        )
    )


def paraphrase_feedback(
    *,
    level: int,
    text: str,
    word_count: int,
    sentence_count: int,
    source_text: str | None = None,
    learner_level: int | None = None,
) -> dict[str, Any]:
    ll = learner_level if learner_level is not None else level
    rules = (
        "Level 1: the student should write 2–5 complete sentences.\n"
        if level == 1
        else (
            "Level 2: target length 50–70 words.\n"
            if level == 2
            else "Level 3: target length 70–120 words.\n"
        )
    )
    user_parts = [
        rules,
        f"Reported stats: {sentence_count} sentences, {word_count} words.\n",
    ]
    if source_text:
        user_parts.append(
            "ORIGINAL TEXT (the student should paraphrase this in their own words, not copy it):\n"
            f"{source_text}\n\n"
        )
    user_parts.append(f"STUDENT'S VERSION:\n{text}\n")
    user = "".join(user_parts)
    system = PARAPHRASE_SYSTEM + feedback_language_instruction(ll)
    return _with_spans(
        fetch_openai_json_messages(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.45,
            max_completion_tokens=3072,
        )
    )


def count_sentences(text: str) -> int:
    parts = re.split(r"[.!?]+", text or "")
    return len([p for p in parts if p.strip()])
