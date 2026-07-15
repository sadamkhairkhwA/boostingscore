"""Shared helpers for academic reading test payloads."""
from __future__ import annotations


def q(
    qid: int,
    part: int,
    qtype: str,
    section_heading: str,
    section_subtype: str,
    instruction: str,
    prompt: str,
    options: list[str] | None,
    correct: str,
    accepted: list[str] | None = None,
    explanation: str = "",
    summary_html: str | None = None,
):
    return {
        "id": qid,
        "part": part,
        "type": qtype,
        "section_heading": section_heading,
        "section_subtype": section_subtype,
        "instruction": instruction,
        "prompt": prompt,
        "options": options or [],
        "correct": correct,
        "accepted": accepted or [correct],
        "explanation": explanation,
        "summary_html": summary_html,
    }


def build_payload(
    *,
    test_number: int,
    title_bar: str,
    part1_html: str,
    part2_html: str,
    part3_html: str,
    instructions: dict,
    part_meta: dict,
    questions: list,
    summary_intro_html: str = "",
    results_meta: dict | None = None,
    result_meta_by_id: dict | None = None,
) -> dict:
    from reading.academic_test_data import default_skill_for_question

    meta = result_meta_by_id or {}

    def enrich(question: dict) -> dict:
        d = dict(question)
        m = meta.get(int(question["id"]), {})
        d["skill"] = m.get("skill") or default_skill_for_question(question)
        d["why_wrong"] = (m.get("why_wrong") or "You missed a key detail in the passage").strip()
        d["passage_ref"] = (m.get("passage_ref") or d.get("explanation") or "").strip()
        d["common_mistake"] = (m.get("common_mistake") or "").strip()
        return d

    return {
        "testTitleBar": title_bar,
        "timeLimitSeconds": 60 * 60,
        "passages": {
            "1": part1_html.strip(),
            "2": part2_html.strip(),
            "3": part3_html.strip(),
        },
        "instructions": instructions,
        "partMeta": part_meta,
        "summaryIntroHtml": summary_intro_html.strip(),
        "questions": [enrich(dict(item)) for item in questions],
        "resultsMeta": results_meta
        or {
            "part1Title": part_meta[1]["subtitle"],
            "part2Title": part_meta[2]["subtitle"],
            "part3Title": part_meta[3]["subtitle"],
        },
    }
