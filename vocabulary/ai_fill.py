"""OpenAI: fill definition + example for a vocabulary word (JSON over HTTP)."""
import json
import logging
import os
import re
from typing import Any

import httpx
from django.conf import settings

from boostingscore.openai_key import resolve_openai_api_key

logger = logging.getLogger(__name__)

SYSTEM = """You help IELTS learners build vocabulary.
Return a single JSON object only (no markdown fences) with keys:
- "definition": concise English definition (1-2 sentences)
- "example_sentence": one natural example sentence using the word in context

Use academic/neutral tone appropriate to the stated level (1=simpler, 3=more advanced)."""


def _resolve_api_key() -> str:
    return resolve_openai_api_key()


def _post(api_key: str, base_url: str, org: str | None, project: str | None, timeout: float, body: dict) -> dict:
    payload = json.dumps(body, ensure_ascii=False, allow_nan=False)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    if org:
        headers["OpenAI-Organization"] = org
    if project:
        headers["OpenAI-Project"] = project
    url = base_url.rstrip("/") + "/chat/completions"
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=headers, content=payload.encode("utf-8"))
    if r.status_code != 200:
        raise RuntimeError(f"OpenAI {r.status_code}: {r.text[:1200]}")
    return r.json()


def _strip_fence(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text)
    return m.group(1).strip() if m else text


def _type_it_chat_completion_text(
    *,
    api_key: str,
    base_url: str,
    org: str | None,
    project: str | None,
    timeout: float,
    model: str,
    system: str,
    user_msg: str,
    use_json_object: bool,
) -> str:
    """Prefer official ``openai`` SDK; fall back to httpx on failure."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg},
    ]
    try:
        from openai import OpenAI

        kwargs: dict[str, Any] = {"api_key": api_key, "timeout": timeout}
        bu = (base_url or "").strip().rstrip("/")
        if bu:
            kwargs["base_url"] = bu
        if org:
            kwargs["organization"] = org
        if project:
            kwargs.setdefault("default_headers", {})["OpenAI-Project"] = project
        client = OpenAI(**kwargs)
        create_kw: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": 0.35,
            "max_completion_tokens": 1200,
        }
        if use_json_object:
            create_kw["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(**create_kw)
        return (response.choices[0].message.content or "").strip()
    except Exception as exc:
        logger.warning(
            "OpenAI SDK chat.completions failed (%s); falling back to httpx.",
            exc,
            exc_info=logger.isEnabledFor(logging.DEBUG),
        )

    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": 0.35,
        "max_completion_tokens": 1200,
    }
    if use_json_object:
        body["response_format"] = {"type": "json_object"}
    data = _post(api_key, base_url, org, project, timeout, body)
    return (data["choices"][0]["message"].get("content") or "").strip()


def _parse_type_it_response_json(raw_text: str) -> dict[str, Any]:
    """Parse model JSON; tolerate markdown fences; never raise."""
    content = (raw_text or "").strip()
    candidates: list[str] = []
    fenced = _strip_fence(content)
    if fenced != content:
        candidates.append(fenced)
    candidates.append(content)
    if "```" in content:
        parts = content.split("```")
        if len(parts) >= 2:
            mid = parts[1].strip()
            if mid.lower().startswith("json"):
                mid = mid[4:].lstrip()
            candidates.append(mid.strip())
    for attempt in candidates:
        s = attempt.strip()
        if not s:
            continue
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            continue
    return {
        "band": "6.0",
        "bandClass": "mid",
        "title": "Good attempt",
        "subtitle": "AI feedback available",
        "correctedVersion": content[:4000] if content else "",
        "workedWell": "Sentence received",
        "toImprove": "Try to use more academic vocabulary",
        "workedChips": [],
        "improveChips": [],
        "errors": [],
        "ieltsTip": "",
        "improved": content[:4000] if content else "",
        "strength_text": "Sentence received",
        "improve_text": "Try to use more academic vocabulary",
        "strengths": [],
        "improvements": [],
        "ielts_tip": "",
    }


def _type_it_coerce_band_float(raw: Any, *, ielts_mode: bool, default: float = 5.0) -> float:
    if not ielts_mode:
        return default
    if raw is None:
        return default
    if isinstance(raw, str) and raw.strip().lower() in ("", "null", "none"):
        return default
    try:
        x = float(raw)
    except (TypeError, ValueError):
        return default
    return max(1.0, min(9.0, x))


def _type_it_infer_band_class(band: float) -> str:
    if band < 5.0:
        return "low"
    if band < 7.0:
        return "mid"
    return "hi"


def _normalize_type_it_session_payload(
    parsed: dict[str, Any], *, ielts_mode: bool
) -> dict[str, Any]:
    """Map model JSON (new or legacy keys) to API fields used by the Type it UI."""
    improved = (
        str(parsed.get("correctedVersion") or parsed.get("improved") or "").strip()
    )
    strength_text = str(
        parsed.get("workedWell") or parsed.get("strength_text") or ""
    ).strip()
    improve_text = str(
        parsed.get("toImprove") or parsed.get("improve_text") or ""
    ).strip()

    def _arr_from(*keys: str) -> list[str]:
        for k in keys:
            v = parsed.get(k)
            if isinstance(v, list):
                return [str(x).strip() for x in v if str(x).strip()]
        return []

    strengths = _arr_from("workedChips", "strengths")
    improvements = _arr_from("improveChips", "improvements")
    errors = _arr_from("errors")

    ielts_tip = str(
        parsed.get("ieltsTip") or parsed.get("ielts_tip") or ""
    ).strip()
    if not ielts_mode:
        ielts_tip = ""

    band_f = _type_it_coerce_band_float(parsed.get("band"), ielts_mode=ielts_mode)

    bc_raw = str(
        parsed.get("bandClass") or parsed.get("band_class") or ""
    ).strip().lower()
    if bc_raw in ("low", "mid", "hi"):
        band_class = bc_raw
    else:
        band_class = _type_it_infer_band_class(band_f)

    title = str(parsed.get("title") or "").strip() or "Result"
    subtitle = str(parsed.get("subtitle") or "").strip()

    return {
        "band": band_f,
        "band_class": band_class,
        "band_hidden": not ielts_mode,
        "title": title,
        "subtitle": subtitle,
        "improved": improved,
        "strength_text": strength_text,
        "improve_text": improve_text,
        "strengths": strengths,
        "improvements": improvements,
        "errors": errors,
        "ielts_tip": ielts_tip,
        "correctedVersion": improved,
        "workedWell": strength_text,
        "toImprove": improve_text,
        "workedChips": strengths,
        "improveChips": improvements,
        "ieltsTip": ielts_tip,
    }


def generate_definition_and_example(
    *,
    word: str,
    topic: str,
    level: int,
    model: str | None = None,
) -> dict[str, str]:
    api_key = _resolve_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = (model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_TIMEOUT", "60"))

    user_msg = (
        f'Word: "{word.strip()}"\n'
        f"Topic area: {topic}\n"
        f"Difficulty level: {level} (1=basic, 3=advanced)\n"
        "Write definition and one example sentence."
    )

    base_body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.5,
        "max_completion_tokens": 500,
    }

    data = None
    for use_rf in (True, False):
        body = dict(base_body)
        if use_rf:
            body["response_format"] = {"type": "json_object"}
        try:
            data = _post(api_key, base_url, org, project, timeout, body)
            break
        except RuntimeError as exc:
            if use_rf and "400" in str(exc):
                continue
            raise

    if data is None:
        raise RuntimeError("OpenAI request failed.")

    text = (data["choices"][0]["message"].get("content") or "").strip()
    text = _strip_fence(text)
    parsed = json.loads(text)
    return {
        "definition": str(parsed.get("definition") or "").strip(),
        "example_sentence": str(parsed.get("example_sentence") or "").strip(),
    }


_TYPE_JSON_RULES = """Rules:
- Be encouraging and practical; keep every string field brief (no long essays).
- Do not be overly strict on minor grammar if meaning and word use are fine.
- Prioritise natural, appropriate vocabulary use.
- Output MUST be one JSON object only — no markdown code fences, no text before or after."""

# Sentence-level only — reward lexical resource; do not score like a full Task 2 essay.
_SINGLE_SENTENCE_BAND_GUIDE = """ESTIMATED_BAND — vocabulary practice, ONE sentence only (not a full IELTS essay):
Score sentence-level lexical resource, grammatical accuracy, and naturalness. Do NOT penalise harshly for missing essay development, cohesion, or multiple ideas — one sentence cannot show those.

REWARD strong vocabulary: if the student uses accurate, natural, appropriately formal items such as (examples) "exert", "detrimental (impact)", "mitigate", "exacerbate", "considerable", "significant", "safeguard", "poses a threat", etc., and grammar is sound, do NOT default to Band 6.0. Such usage usually supports Band 7.0–7.5 at sentence level when integrated naturally.

Practical anchors (half-bands):
- Band 5.0–5.5: understandable but simple, awkward, or limited vocabulary; errors or vagueness may appear.
- Band 6.0–6.5: correct grammar overall; common vocabulary; limited sophistication or range for academic writing.
- Band 7.0–7.5: clear, natural sentence with strong or precise vocabulary used correctly — typical target for a polished practice line with good lexis.
- Band 8.0+: exceptionally natural, polished, precise, advanced control — rare for this feature.
- Band 8.5–9.0: almost never for one short sentence; only if exceptional precision and near-native control in that line.

Calibration example (sentence-level): "Landfills exert a detrimental impact on the environment." — strong collocations and formal lexis; if accurate and natural, estimated_band is usually 7.0–7.5, NOT 6.0.

Placement (app Beginner/Standard/Advanced): affects how simple your short_feedback/tips are written — it must NOT lower estimated_band. Judge the sentence objectively.

Ceiling: both estimated_band and improved_band — avoid 8.5/9.0 unless truly exceptional; 8.0+ still uncommon."""

_DUAL_BAND_EXAMPLE_RULES = """REWRITE AND DUAL BAND (IELTS example mode):
1) Score the ORIGINAL student sentence → "estimated_band" (same rubric as above). Treat the band as a number for the rules below (e.g. 6.0, 6.5, 7.5).

MANDATORY THRESHOLDS:
- If estimated_band < 6.5: rewrite_offered MUST be true. improved_sentence MUST be non-empty (exactly one sentence, must include TARGET WORD). improved_band MUST be strictly greater than 7.0 (e.g. 7.5 or 8.0) — write a model line with clearly stronger academic lexis and natural collocations so the score reflects above Band 7. short_feedback should briefly say you are showing a higher-band example to aim for.
- If estimated_band > 7.0: rewrite_offered MUST be false. improved_sentence MUST be "" and improved_band MUST be "". sentence_already_strong MUST be true. Do not offer a rewrite (the line is already above the practice target).
- If 6.5 ≤ estimated_band ≤ 7.0: use judgement — offer rewrite_offered true only when you can genuinely raise quality; if true, improved_band should exceed estimated_band when lexis is upgraded; if no real gain, rewrite_offered false and explain.

2) When rewrite_offered is true: improved_sentence must never be weaker or more basic than the original unless the original was wrong.

3) "sentence_already_strong": true when rewrite_offered is false because the original is already strong (including the >7.0 case), or no worthwhile rewrite; false when you offer a rewrite.

short_feedback must align with rewrite_offered and bands.

HARD RULE: If improved_sentence has clearly stronger academic vocabulary than the original, improved_band MUST exceed estimated_band (unless a rare counter-case explained in short_feedback).

Use half-bands. Avoid inflating weak originals in estimated_band just to skip writing an improved line."""


def _learner_placement(level: int) -> tuple[int, str]:
    """Map raw level to 1–3 and label (matches placement / UserProfile.level)."""
    try:
        n = int(level)
    except (TypeError, ValueError):
        n = 2
    lv = n if n in (1, 2, 3) else 2
    names = {1: "Beginner", 2: "Standard", 3: "Advanced"}
    return lv, names[lv]


def _system_learner_reading_level(level: int) -> str:
    """Short system reminder: feedback stays approachable; model sentence may stretch higher."""
    lv, name = _learner_placement(level)
    if lv == 1:
        return (
            f"READING LEVEL: The learner is {name} (placement level 1). "
            "Write short_feedback, vocabulary_tip, reference_definition, clear_definition, simple_ielts_example, and alternatives "
            "in VERY SIMPLE English (short sentences, common words). "
            "EXCEPTION — improved_sentence: this is a study model; it SHOULD use clearer, more precise or slightly more formal "
            "wording than the student wrote when that helps Band — still ONE sentence, not fancy for its own sake."
        )
    if lv == 2:
        return (
            f"READING LEVEL: The learner is {name} (placement level 2). "
            "Use clear intermediate English (B1–B2) in all JSON strings. Some richer words are fine if natural."
        )
    return (
        f"READING LEVEL: The learner is {name} (placement level 3). "
        "You may use more sophisticated vocabulary and nuance in JSON strings where it helps."
    )


def _user_learner_placement_block(level: int) -> str:
    """Strong, task-specific guidance appended to the user message."""
    lv, name = _learner_placement(level)
    if lv == 1:
        return (
            f"LEARNER_PLACEMENT: {lv} — {name} (from the app's vocabulary placement test).\n"
            "Field rules:\n"
            "- short_feedback, vocabulary_tip: very simple words; 1–2 short sentences.\n"
            "- reference_definition / clear_definition: simple English a beginner can read.\n"
            "- simple_ielts_example: one natural but SIMPLE sentence.\n"
            "- alternatives: common, easy words or short phrases (avoid obscure jargon).\n"
            "- BAND (IELTS ON): estimated_band is objective sentence quality — placement does NOT lower it; strong lexis can be 7.0–7.5.\n"
            "- If estimated_band < 6.5: model MUST still give improved_sentence (advanced English OK) with improved_band > 7.0. If > 7.0: no rewrite.\n"
            "- rewrite_offered false when no genuine improvement; never replace strong academic English with a simpler paraphrase.\n"
        )
    if lv == 2:
        return (
            f"LEARNER_PLACEMENT: {lv} — {name}.\n"
            "Use intermediate English throughout JSON text fields. "
            "If IELTS mode on: objective bands per guide; strong lexis often 7.0–7.5. rewrite_offered only when genuinely better.\n"
        )
    return (
        f"LEARNER_PLACEMENT: {lv} — {name}.\n"
        "You may use advanced vocabulary and nuance in JSON text fields. "
        "If IELTS mode on: sentence-level scoring; strong academic lines can be 7.0–7.5+. No false downgrades. Offer rewrite only if better.\n"
    )


def _system_check_example(*, ielts_mode: bool, learner_level: int) -> str:
    lv, _ = _learner_placement(learner_level)
    band_line = (
        '- "estimated_band": string — half-band for the STUDENT\'s ORIGINAL only.\n'
        '- "improved_band": string — half-band for improved_sentence only; if rewrite_offered is false, use "".\n'
        '- "rewrite_offered": boolean — MUST be true if estimated_band < 6.5; MUST be false if estimated_band > 7.0; otherwise per dual-band rules.\n'
        '- "sentence_already_strong": boolean — true when rewrite_offered is false (required true when estimated_band > 7.0).'
        if ielts_mode
        else '- "estimated_band": ""\n'
        '- "improved_band": ""\n'
        '- "rewrite_offered": false\n'
        '- "sentence_already_strong": false'
    )
    alt_line = (
        '- "alternatives": array of 2 or 3 strings — better words or short phrases the student could use in similar contexts (or [] if not helpful).'
        if ielts_mode
        else '- "alternatives": array of 0–2 strings, or [] — only if clearly useful; keep it light.'
    )
    if ielts_mode:
        if lv == 1:
            focus = (
                "IELTS Mode ON: keep tips and feedback in very simple English for this Beginner, "
                "but improved_sentence is allowed to sound a bit more IELTS-formal as a clear upgrade example."
            )
        else:
            focus = (
                "IELTS Mode ON: comment on band-style clarity, academic/formal tone where fitting, and natural collocations."
            )
    else:
        focus = "IELTS Mode OFF: simple, friendly feedback; skip band-style detail."
    tone = _system_learner_reading_level(learner_level)
    band_block = (
        f"{_SINGLE_SENTENCE_BAND_GUIDE}\n\n{_DUAL_BAND_EXAMPLE_RULES}\n\n" if ielts_mode else ""
    )
    return f"""You are an IELTS vocabulary coach. {focus}
{tone}
The student wrote an English sentence using the TARGET WORD. Judge natural use: correct word form, sensible meaning, acceptable grammar (minor slips are OK).
First score the ORIGINAL; then decide if a genuine improvement exists — never offer a weaker or oversimplified "improvement" for strong academic lines.
{_TYPE_JSON_RULES}

{band_block}COLLOCATION (IELTS): Comment on how the TARGET WORD combines with nearby words in the student's sentence.
- "collocation_advice": string — one short sentence. If collocations are natural and appropriate, praise briefly. If weak, odd, or un-IELTS-like, say so and point toward better patterns — keep it short.
- "natural_collocations": array of 2–3 strings — useful IELTS-style collocations with the target word (e.g. "mitigate the effects", "adverse consequences").

Return JSON with exactly these keys:
- "is_correct": boolean — true if good enough for practice; false if word wrong/missing/misused or grammar blocks meaning
- "short_feedback": string — 1–2 short sentences; align with bands and rewrite_offered
- "improved_sentence": string — ONE sentence with TARGET WORD if rewrite_offered true; otherwise "" (empty)
{band_line}
- "vocabulary_tip": string — one short tip (or encouragement if already strong)
{alt_line}
- "reference_definition": string — concise definition of the TARGET WORD (1–2 sentences)
- "collocation_advice": string — as above
- "natural_collocations": array of 2–3 strings — as above"""


def _system_check_definition(*, ielts_mode: bool, learner_level: int) -> str:
    lv, _ = _learner_placement(learner_level)
    if ielts_mode:
        if lv == 1:
            focus = (
                "IELTS Mode ON: relate tips to IELTS study, but keep all wording VERY SIMPLE for this Beginner — no heavy academic jargon in your JSON text."
            )
        else:
            focus = "IELTS Mode ON: tie tips to academic word use and IELTS-style phrasing."
    else:
        focus = "IELTS Mode OFF: keep tips simple and supportive."
    tone = _system_learner_reading_level(learner_level)
    return f"""You are an IELTS vocabulary coach. {focus}
{tone}
The student wrote their own definition of the TARGET WORD. Compare to the official deck definition when provided.
{_TYPE_JSON_RULES}
COLLOCATION (IELTS): Help with how the word is used in real phrases.
- "collocation_advice": string — one short sentence. Praise if their definition shows awareness of natural word partners; if not, briefly note useful patterns — IELTS-focused, short.
- "natural_collocations": array of 2–3 strings — natural collocations with the TARGET WORD for Task 2 / academic English.

Return JSON with exactly these keys:
- "is_correct": boolean — true if the definition captures the main meaning; false if wrong or misses the core sense
- "short_feedback": string — 1–2 short sentences
- "clear_definition": string — the clearest reference definition (1–2 sentences; align with the deck when accurate)
- "simple_ielts_example": string — one natural example sentence using the word (IELTS-style if mode on)
- "vocabulary_tip": string — one short tip
- "collocation_advice": string — as above
- "natural_collocations": array of 2–3 strings — as above"""


def _coerce_bool(val: Any) -> bool:
    if isinstance(val, str):
        return val.strip().lower() in ("true", "yes", "1")
    return bool(val)


def _normalize_band(s: str) -> str:
    t = (s or "").strip()
    if not t:
        return ""
    t = re.sub(r"^band\s*", "", t, flags=re.I).strip()
    return t


def _band_to_float(s: str) -> float | None:
    t = _normalize_band(s)
    if not t:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _normalize_alternatives(raw: Any, max_n: int = 5) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for x in raw:
        s = str(x).strip()
        if s and s not in out:
            out.append(s)
        if len(out) >= max_n:
            break
    return out


def _parse_type_practice_json(text: str) -> dict[str, Any]:
    text = _strip_fence(text)
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("expected JSON object")
    return parsed


def normalize_type_practice_result(
    parsed: dict[str, Any],
    mode: str,
    *,
    ielts_mode: bool = True,
) -> dict[str, Any]:
    """Build API-safe dict from model JSON; fills legacy keys for older clients."""
    mode = (mode or "example").strip().lower()
    if mode not in ("example", "definition"):
        mode = "example"

    is_correct = _coerce_bool(parsed.get("is_correct", parsed.get("correct")))

    if mode == "definition":
        short_feedback = str(parsed.get("short_feedback") or parsed.get("feedback") or "").strip()
        clear_def = str(parsed.get("clear_definition") or parsed.get("meaning") or "").strip()
        example_s = str(parsed.get("simple_ielts_example") or "").strip()
        tip = str(parsed.get("vocabulary_tip") or "").strip()
        colloc_adv = str(parsed.get("collocation_advice") or "").strip()
        collocs = _normalize_alternatives(parsed.get("natural_collocations"), max_n=3)
        return {
            "mode": "definition",
            "is_correct": is_correct,
            "correct": is_correct,
            "short_feedback": short_feedback,
            "feedback": short_feedback,
            "clear_definition": clear_def,
            "simple_ielts_example": example_s,
            "vocabulary_tip": tip,
            "collocation_advice": colloc_adv,
            "natural_collocations": collocs,
            "improved_sentence": "",
            "estimated_band": "",
            "improved_band": "",
            "rewrite_offered": False,
            "sentence_already_strong": False,
            "alternatives": [],
            "meaning": clear_def,
        }

    short_feedback = str(parsed.get("short_feedback") or parsed.get("feedback") or "").strip()
    improved = str(parsed.get("improved_sentence") or "").strip()
    tip = str(parsed.get("vocabulary_tip") or "").strip()
    alts = _normalize_alternatives(parsed.get("alternatives"))
    ref_mean = str(parsed.get("reference_definition") or parsed.get("meaning") or "").strip()
    colloc_adv = str(parsed.get("collocation_advice") or "").strip()
    collocs = _normalize_alternatives(parsed.get("natural_collocations"), max_n=3)

    raw_ro = parsed.get("rewrite_offered")
    if raw_ro is None:
        rewrite_offered = bool(improved)
    else:
        rewrite_offered = _coerce_bool(raw_ro)

    if ielts_mode:
        band = _normalize_band(
            str(parsed.get("estimated_band") or parsed.get("original_band") or "")
        )
        imp_band = _normalize_band(str(parsed.get("improved_band") or ""))
    else:
        band = ""
        imp_band = ""
        rewrite_offered = bool(improved)

    if not rewrite_offered:
        improved = ""
        imp_band = ""
    elif not improved:
        rewrite_offered = False
        imp_band = ""

    sas_raw = parsed.get("sentence_already_strong")
    sentence_already_strong = _coerce_bool(sas_raw) if sas_raw is not None else False
    if rewrite_offered:
        sentence_already_strong = False
    if not ielts_mode:
        sentence_already_strong = False

    if ielts_mode and band:
        eb_f = _band_to_float(band)
        if eb_f is not None and eb_f > 7.0:
            rewrite_offered = False
            improved = ""
            imp_band = ""
            sentence_already_strong = True

    return {
        "mode": "example",
        "is_correct": is_correct,
        "correct": is_correct,
        "short_feedback": short_feedback,
        "feedback": short_feedback,
        "improved_sentence": improved,
        "estimated_band": band,
        "improved_band": imp_band,
        "rewrite_offered": rewrite_offered,
        "sentence_already_strong": sentence_already_strong,
        "vocabulary_tip": tip,
        "collocation_advice": colloc_adv,
        "natural_collocations": collocs,
        "alternatives": alts,
        "clear_definition": "",
        "simple_ielts_example": "",
        "meaning": ref_mean,
    }


def check_type_practice(
    *,
    word: str,
    topic: str,
    level: int,
    student_text: str,
    deck_definition: str,
    deck_example: str,
    mode: str,
    ielts_mode: bool = True,
    model: str | None = None,
) -> dict[str, Any]:
    api_key = _resolve_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    mode = (mode or "example").strip().lower()
    if mode not in ("example", "definition"):
        mode = "example"

    model = (model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_TIMEOUT", "60"))

    ss = student_text.strip()
    im = "ON" if ielts_mode else "OFF"
    lv, lv_name = _learner_placement(level)
    placement_user = _user_learner_placement_block(level)
    if mode == "definition":
        system = _system_check_definition(ielts_mode=ielts_mode, learner_level=lv)
        user_msg = (
            f"{placement_user}\n"
            f"IELTS_MODE: {im}\n"
            f'TARGET WORD: "{word.strip()}"\n'
            f"Topic area: {topic}\n"
            f"Learner vocabulary placement: {lv} ({lv_name}) — this is the student's level in the app, not the word card.\n\n"
            f"OFFICIAL DEFINITION FROM THE DECK (gold standard when provided):\n"
            f"{(deck_definition or '').strip() or '(not provided — infer an accurate definition yourself)'}\n\n"
            f"Official example from the deck (optional context):\n"
            f"{(deck_example or '').strip() or '(not provided)'}\n\n"
            f"STUDENT'S DEFINITION (verbatim):\n{ss}\n\n"
            "Judge whether the student's definition is substantially correct. Fill every JSON key."
        )
    else:
        system = _system_check_example(ielts_mode=ielts_mode, learner_level=lv)
        user_msg = (
            f"{placement_user}\n"
            f"IELTS_MODE: {im}\n"
            f'TARGET WORD (the student must use this word): "{word.strip()}"\n'
            f"Topic area: {topic}\n"
            f"Learner vocabulary placement: {lv} ({lv_name}) — this is the student's level in the app, not the word card.\n\n"
            f"Official definition from the course deck (use to judge meaning):\n"
            f"{(deck_definition or '').strip() or '(not provided)'}\n\n"
            f"Official example from the deck (optional reference):\n"
            f"{(deck_example or '').strip() or '(not provided)'}\n\n"
            f"ORIGINAL_STUDENT_SENTENCE (verbatim — score this alone as estimated_band):\n{ss}\n\n"
            "Decide if the student used the target word acceptably. "
            "Apply MANDATORY THRESHOLDS: if estimated_band < 6.5 you MUST return rewrite_offered true, a non-empty improved_sentence, and improved_band > 7.0; "
            "if estimated_band > 7.0 you MUST return rewrite_offered false and empty improved fields. Fill every JSON key."
        )

    base_body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.35,
        "max_completion_tokens": 1250,
    }

    data = None
    last_err: RuntimeError | None = None
    for use_rf in (True, False):
        body = dict(base_body)
        if use_rf:
            body["response_format"] = {"type": "json_object"}
        try:
            data = _post(api_key, base_url, org, project, timeout, body)
            last_err = None
            break
        except RuntimeError as exc:
            last_err = exc
            if use_rf and "400" in str(exc):
                continue
            raise

    if data is None:
        raise last_err or RuntimeError("OpenAI request failed.")

    text = (data["choices"][0]["message"].get("content") or "").strip()
    try:
        parsed = _parse_type_practice_json(text)
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid model JSON: {exc}") from exc

    return normalize_type_practice_result(parsed, mode, ielts_mode=ielts_mode)


def evaluate_type_it_session(
    *,
    word: str,
    definition: str,
    part_of_speech: str = "",
    topic_label: str = "",
    student_text: str,
    mode: str,
    ielts_mode: bool,
    level: int,
    model: str | None = None,
) -> dict[str, Any]:
    """
    Type it session evaluation for Boosting Score: structured JSON + optional IELTS band.

    ``level`` is accepted for API compatibility with callers.
    ``part_of_speech`` / ``topic_label`` are shown to the model for context only.
    """
    api_key = _resolve_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    mode = (mode or "sentence").strip().lower()
    if mode not in ("sentence", "definition"):
        mode = "sentence"

    model = (model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_TIMEOUT", "60"))

    w = (word or "").strip().replace("\n", " ")[:200]
    pos_disp = (part_of_speech or "word").strip().replace("\n", " ")[:60] or "word"
    top_disp = (topic_label or "general").strip().replace("\n", " ")[:80] or "general"
    mode_wrote = (
        "an example sentence that uses this word naturally"
        if mode == "sentence"
        else "their own definition of this word (a paraphrase)"
    )
    if ielts_mode:
        ielts_instruction = (
            "Apply IELTS Writing-style bands from 1.0 to 9.0. Be strict: answers that are "
            "very short, vague, informal, or grammatically weak must sit in low or lower-mid "
            "bands unless the writing clearly earns higher."
        )
    else:
        ielts_instruction = (
            'IELTS band scoring is OFF. In your JSON set "band" to null and "bandClass" '
            'to "mid". Still judge correctness, completeness, register, and grammar; fill '
            "errors, correctedVersion, workedWell, toImprove, workedChips, and improveChips. "
            'Set "ieltsTip" to an empty string.'
        )

    system = f"""You are an expert IELTS vocabulary coach inside a learning app called Boosting Score.

The student is practising the word {json.dumps(w)} ({json.dumps(pos_disp)}, {json.dumps(top_disp)} topic).
They wrote {mode_wrote}.
{ielts_instruction}

Evaluate their response on these criteria:
1. CORRECTNESS — is the meaning accurate?
2. COMPLETENESS — does it cover the full meaning?
3. ACADEMIC REGISTER — is the language formal enough for IELTS?
4. GRAMMAR — is the sentence grammatically correct?

Respond ONLY with a valid JSON object. No markdown, no extra text, no explanation outside the JSON:
{{
  "band": "6.5",
  "bandClass": "mid",
  "title": "Developing",
  "subtitle": "One short sentence summarising the main strength or weakness",
  "errors": ["short error label 1", "short error label 2"],
  "correctedVersion": "A complete, academically appropriate corrected sentence.",
  "workedWell": "One sentence praising what the student did correctly.",
  "workedChips": ["Positive label 1", "Positive label 2"],
  "toImprove": "One sentence explaining the most important thing to fix.",
  "improveChips": ["Issue label 1", "Issue label 2"],
  "ieltsTip": "One specific, actionable IELTS writing tip directly related to their mistake."
}}

Strict rules:
- band: a number from 1.0 to 9.0 as a string, e.g. "7.0". If IELTS mode is off, set to null.
- bandClass: exactly "low" if band < 5, "mid" if band 5–6.5, "hi" if band 7 or above. If IELTS mode is off, use "mid".
- title: one of "Needs more work", "Developing", "Good attempt", "Well done", "Excellent".
- errors: 1 to 3 short chip labels (max 5 words each) describing specific mistakes.
- correctedVersion: must be a full, complete sentence. Academic vocabulary. No informal language.
- workedChips: 1 to 2 short positive labels, e.g. "Has a subject", "Relevant vocabulary".
- improveChips: 1 to 3 short issue labels, e.g. "Too informal", "Lacks detail", "No consequence clause".
- ieltsTip: must be specific to THIS word and THIS mistake — not generic advice (empty string if IELTS mode is off).
- If the student wrote something completely off-topic or nonsensical, set band to "3.0", bandClass to "low", title to "Needs more work".
"""

    user_msg = f"""Word: {word.strip()}
Part of speech: {pos_disp}
Topic label: {top_disp}
Definition: {(definition or "").strip() or "(not provided)"}
Mode (machine): {mode}
IELTS mode (machine): {ielts_mode}
Student wrote: {json.dumps((student_text or "").strip()[:4000])}

Return JSON only matching the schema in the system message."""

    text = ""
    last_err: Exception | None = None
    for use_rf in (True, False):
        try:
            chunk = _type_it_chat_completion_text(
                api_key=api_key,
                base_url=base_url,
                org=org,
                project=project,
                timeout=timeout,
                model=model,
                system=system,
                user_msg=user_msg,
                use_json_object=use_rf,
            )
            if (chunk or "").strip():
                text = chunk
                break
        except Exception as exc:
            last_err = exc
            es = str(exc)
            if use_rf and (
                "400" in es
                or "unsupported" in es.lower()
                or "response_format" in es.lower()
            ):
                continue
            raise RuntimeError(es) from exc
    else:
        raise RuntimeError(
            str(last_err or "OpenAI request failed or returned empty content.")
        )

    parsed = _parse_type_it_response_json(text)
    return _normalize_type_it_session_payload(parsed, ielts_mode=ielts_mode)
