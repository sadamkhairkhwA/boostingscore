"""Timed reading drills — one passage per part from Academic Test 1."""
from __future__ import annotations

from .academic_test_data import (
    INSTRUCTIONS,
    PART1_HTML,
    PART2_HTML,
    PART3_HTML,
    PART_META,
    QUESTIONS,
    answer_matches,
    band_from_score,
    enrich_question_for_client,
)

TIMED_DRILL_MINUTES = 20

PASSAGES = {1: PART1_HTML.strip(), 2: PART2_HTML.strip(), 3: PART3_HTML.strip()}

DRILL_OPTIONS = [
    {
        "part": 1,
        "title": "Part 1 — Roman concrete",
        "subtitle": "14 questions · ~20 minutes",
        "question_count": 14,
    },
    {
        "part": 2,
        "title": "Part 2 — Flexible working",
        "subtitle": "13 questions · ~20 minutes",
        "question_count": 13,
    },
    {
        "part": 3,
        "title": "Part 3 — Bilingualism",
        "subtitle": "13 questions · ~20 minutes",
        "question_count": 13,
    },
]


def get_timed_drill_payload(part: int) -> dict:
    if part not in (1, 2, 3):
        raise ValueError("part must be 1, 2, or 3")
    meta = PART_META[part]
    questions = [enrich_question_for_client(dict(q)) for q in QUESTIONS if q["part"] == part]
    return {
        "part": part,
        "testTitleBar": f"Timed drill — {meta['label']}",
        "timeLimitSeconds": TIMED_DRILL_MINUTES * 60,
        "passages": {str(part): PASSAGES[part]},
        "instructions": {str(part): INSTRUCTIONS[part]},
        "partMeta": {str(part): meta},
        "summaryIntroHtml": "",
        "questions": questions,
        "singlePart": True,
        "part": part,
    }


def score_part_answers(part: int, answers: dict) -> tuple[int, int]:
    score = total = 0
    for q in QUESTIONS:
        if q["part"] != part:
            continue
        total += 1
        if answer_matches(q, answers.get(str(q["id"]), "")):
            score += 1
    return score, total


def band_for_part_score(score: int, total: int) -> str:
    if not total:
        return "—"
    scaled = round(score / total * 40)
    return band_from_score(scaled)
