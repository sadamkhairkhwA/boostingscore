"""OpenAI batch enrichment and validation for IELTS vocabulary entries."""

from __future__ import annotations

import json
import re
import time
from typing import Any

from vocabulary.word_curation import is_basic_lemma

LEVEL_BAND = {
    1: "Band 5–6 core topic vocabulary",
    2: "Band 6–7 topic collocations and academic phrases",
    3: "Band 7+ less common lexis and precise academic terms",
}

TOPIC_LABELS = {
    "environment": "Environment",
    "health": "Health",
    "technology": "Technology",
    "education": "Education",
    "society": "Society (crime, media, globalisation, culture, family, government)",
    "travel": "Travel and transport",
    "science": "Science",
    "business": "Business and work",
}


def build_batch_prompt(items: list[dict[str, Any]]) -> str:
    lines = []
    for it in items:
        lines.append(
            f'- lemma: "{it["word"]}" | topic: {it["topic"]} | level: {it["level"]} '
            f'({LEVEL_BAND.get(it["level"], "IELTS")})'
        )
    word_block = "\n".join(lines)
    return f"""
You are building an IELTS vocabulary bank for Writing Task 2 and Speaking Part 3.

For EACH lemma below, return one JSON object in a JSON array (no markdown, no commentary).

Required fields per item:
- word (exact lemma string)
- part_of_speech (noun, verb, adjective, adverb, or phrase)
- definition (1–2 clear sentences, academic register)
- synonyms (array of exactly 2–3 synonym strings)
- example_sentence (one formal IELTS-style sentence usable in Task 2 or Speaking Part 3)
- collocations (array of 2–4 common collocations)
- ielts_note (one sentence on how to use the word in IELTS)

Rules:
- Every word must be genuinely useful for IELTS (AWL, topic lexis, or band 7+ collocations).
- Do NOT use childish or A1–B1 everyday words.
- Match the assigned level band.
- Return ONLY a JSON array.

Lemmas:
{word_block}
""".strip()


def _extract_json_array(raw: str) -> list[dict]:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    if isinstance(data, dict) and "words" in data:
        data = data["words"]
    if not isinstance(data, list):
        raise ValueError("Expected JSON array")
    return data


def validate_entry(entry: dict, *, expected_word: str, expected_level: int) -> dict | None:
    word = (entry.get("word") or expected_word or "").strip()[:100]
    if not word or is_basic_lemma(word):
        return None
    definition = (entry.get("definition") or "").strip()
    example = (entry.get("example_sentence") or entry.get("example") or "").strip()
    if len(definition) < 20 or len(example) < 30:
        return None
    synonyms = entry.get("synonyms") or []
    if not isinstance(synonyms, list):
        synonyms = []
    synonyms = [str(s).strip() for s in synonyms if str(s).strip()][:3]
    if len(synonyms) < 2:
        return None
    collocations = entry.get("collocations") or []
    if not isinstance(collocations, list):
        collocations = []
    collocations = [str(c).strip() for c in collocations if str(c).strip()][:6]
    pos = (entry.get("part_of_speech") or entry.get("pos") or "word").strip()[:50]
    ielts_note = (entry.get("ielts_note") or "").strip()
    return {
        "word": word,
        "part_of_speech": pos,
        "definition": definition,
        "synonyms": synonyms,
        "example_sentence": example,
        "collocations": collocations,
        "ielts_note": ielts_note,
        "level": expected_level,
    }


def enrich_batch_openai(client, model: str, items: list[dict], *, pause_s: float = 0.5) -> list[dict]:
    """Call OpenAI once for a batch of lemmas. Returns validated entries."""
    if not items:
        return []
    prompt = build_batch_prompt(items)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON arrays for IELTS vocabulary entries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )
    raw = completion.choices[0].message.content or ""
    parsed = _extract_json_array(raw)
    by_word = {(e.get("word") or "").strip().lower(): e for e in parsed}
    out: list[dict] = []
    for it in items:
        key = it["word"].strip().lower()
        entry = by_word.get(key) or next(
            (v for k, v in by_word.items() if k == key), None
        )
        if not entry:
            continue
        validated = validate_entry(
            entry, expected_word=it["word"], expected_level=it["level"]
        )
        if validated:
            out.append(validated)
    if pause_s:
        time.sleep(pause_s)
    return out
