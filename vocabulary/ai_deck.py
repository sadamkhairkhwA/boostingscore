"""OpenAI: generate a batch of vocabulary flashcards from a free-form prompt (Quizlet-style set)."""
import json
import os
import re
from typing import Any

import httpx

from vocabulary.ai_fill import _resolve_api_key
from vocabulary.models import CustomCard

ALLOWED_TOPICS = frozenset(
    {
        CustomCard.TOPIC_ENVIRONMENT,
        CustomCard.TOPIC_HEALTH,
        CustomCard.TOPIC_TECHNOLOGY,
        CustomCard.TOPIC_EDUCATION,
        CustomCard.TOPIC_SOCIETY,
        CustomCard.TOPIC_OTHER,
    }
)

TOPIC_ALIASES = {
    "science": CustomCard.TOPIC_TECHNOLOGY,
    "tech": CustomCard.TOPIC_TECHNOLOGY,
    "medical": CustomCard.TOPIC_HEALTH,
    "medicine": CustomCard.TOPIC_HEALTH,
    "healthcare": CustomCard.TOPIC_HEALTH,
    "nature": CustomCard.TOPIC_ENVIRONMENT,
    "climate": CustomCard.TOPIC_ENVIRONMENT,
    "environmental": CustomCard.TOPIC_ENVIRONMENT,
    "ecology": CustomCard.TOPIC_ENVIRONMENT,
    "culture": CustomCard.TOPIC_SOCIETY,
    "social": CustomCard.TOPIC_SOCIETY,
    "school": CustomCard.TOPIC_EDUCATION,
    "academic": CustomCard.TOPIC_EDUCATION,
    "general": CustomCard.TOPIC_OTHER,
    "misc": CustomCard.TOPIC_OTHER,
    "mixed": CustomCard.TOPIC_OTHER,
}


def normalize_deck_topic(raw: str) -> str:
    t = (raw or "").strip().lower().replace(" ", "_")
    if t in ALLOWED_TOPICS:
        return t
    return TOPIC_ALIASES.get(t, CustomCard.TOPIC_OTHER)


def _post_chat(
    api_key: str, base_url: str, org: str | None, project: str | None, timeout: float, body: dict[str, Any]
) -> dict[str, Any]:
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


MAX_CARDS = 30

SYSTEM = """You generate vocabulary flashcards for English learners.

Return ONE JSON object only (no markdown fences). Shape:
{
  "detected_topic": "<string>",
  "cards": [{"word": "...", "definition": "...", "example_sentence": "..."}]
}

detected_topic MUST be exactly one of these lowercase slugs:
environment, health, technology, education, society, other
Pick the best bucket for the user's request:
- environment: nature, climate, pollution, ecosystems, sustainability
- health: medicine, body, disease, treatment, public health
- technology: science, engineering, digital, AI, innovation
- education: schools, universities, teaching, learning systems, policy
- society: culture, law, cities, work, media, social issues
- other: business, travel, mixed themes, or nothing fits clearly

Rules for cards:
- Each item must be a real vocabulary headword or short phrase in English (max 120 characters).
- Words MUST be directly related to the user's specific request. Match register (IELTS academic, SAT, medical, business, etc.).
- Do NOT output generic study words like: exam, test, study, score, student, homework, learn, practice, book, teacher, classroom, preparation — unless the user explicitly asked for those.
- Good examples: for "IELTS environment vocabulary" use words like detrimental, proliferate, sustainable, ecosystem, biodiversity.
- For "SAT exam vocabulary" use words like ambiguous, ephemeral, benevolent, ubiquitous, eloquent.
- definition: 1–2 clear English sentences. example_sentence: one natural sentence using the word.
- All words in the list must be unique. No numbering inside "word". No markdown inside strings."""


def _parse_cards_from_payload(parsed: Any) -> list[Any]:
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        raw = parsed.get("cards")
        if isinstance(raw, list):
            return raw
        # Alternate key from user-facing spec
        raw = parsed.get("flashcards")
        if isinstance(raw, list):
            return raw
    return []


def generate_flashcard_set(
    *,
    prompt: str,
    count: int,
    level: int,
    topic_slug: str = "",
    topic_label: str = "",
    model: str | None = None,
) -> tuple[list[dict[str, str]], str]:
    api_key = _resolve_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    n = max(1, min(int(count), MAX_CARDS))
    level = level if level in (1, 2, 3) else 2

    model = (model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_DECK_TIMEOUT", "120"))

    bucket = (topic_slug or "other").strip().lower()
    label = (topic_label or bucket).strip() or bucket
    user_msg = (
        f'Generate {n} vocabulary flashcards based on this specific request: "{prompt.strip()}"\n\n'
        f"The learner chose deck topic: **{label}** (slug: {bucket}). Prefer vocabulary that fits this bucket.\n"
        f"Difficulty level {level}: 1 = beginner / everyday; 2 = IELTS-style; 3 = advanced academic.\n"
        f'Each card must have "word", "definition", and "example_sentence".\n'
        f"The words must be directly related to the user's request — not generic study vocabulary.\n"
        f'Put exactly {n} objects in the "cards" array. Set "detected_topic" to "{bucket}" or the closest slug.\n'
        f"Return only the JSON object."
    )

    base_body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.45,
        "max_completion_tokens": min(6000, 220 * n + 500),
    }

    data = None
    for use_rf in (True, False):
        body = dict(base_body)
        if use_rf:
            body["response_format"] = {"type": "json_object"}
        try:
            data = _post_chat(api_key, base_url, org, project, timeout, body)
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

    detected = CustomCard.TOPIC_OTHER
    if isinstance(parsed, dict):
        detected = normalize_deck_topic(str(parsed.get("detected_topic") or parsed.get("topic") or ""))

    raw_cards = _parse_cards_from_payload(parsed)
    if not raw_cards:
        raise RuntimeError('Response missing a "cards" array (or equivalent list).')

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw_cards:
        if not isinstance(item, dict):
            continue
        w = str(item.get("word") or "").strip()
        if not w:
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "word": w[:255],
                "definition": str(item.get("definition") or "").strip()[:4000],
                "example_sentence": str(item.get("example_sentence") or "").strip()[:4000],
            }
        )
        if len(out) >= n:
            break

    if len(out) == 0:
        raise RuntimeError(
            "The model returned no usable cards. Try again with a clearer prompt or fewer cards."
        )

    return out, detected
