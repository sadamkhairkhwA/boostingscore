"""OpenAI-based IELTS Task 2 grading (HTTP JSON, same pattern as reading populate_passages)."""
import json
import os
import re
from typing import Any

import httpx

from boostingscore.openai_key import resolve_openai_api_key

from .feedback_levels import feedback_language_instruction
from .span_schema import SPAN_JSON_RULES_GRADING, normalize_span_list

GRADING_TASK1_SYSTEM_PROMPT = """You are an expert IELTS examiner.
The student wrote an IELTS Academic Task 1 response (describe visual data: chart, graph, table, map, or process).
Grade it on official criteria: Task Achievement (overview, key features, accuracy), Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy.
Return a JSON object only (no markdown, no code fences, no commentary) with exactly these keys:
- band_score: overall band (number 1-9, half bands allowed)
- task_achievement: score out of 9
- coherence: score out of 9
- lexical: score out of 9
- grammar: score out of 9
- feedback: detailed paragraph of feedback (string)
- grammar_mistakes: string listing grammar errors with corrections (multi-line OK)
- vocabulary_suggestions: about 3 stronger academic alternatives (multi-line bullets OK)
""" + SPAN_JSON_RULES_GRADING + """
Task 1 is shorter than Task 2; do not penalize length alone if the prompt is fully addressed. Be honest — do not inflate scores."""

GRADING_SYSTEM_PROMPT = """You are an expert IELTS examiner.
Grade this Task 2 essay on the official IELTS criteria. Return a JSON object only (no markdown, no code fences, no commentary) with exactly these keys:
- band_score: overall band (number 1-9, half bands like 6.5 allowed)
- task_achievement: score out of 9
- coherence: score out of 9
- lexical: score out of 9
- grammar: score out of 9
- feedback: detailed paragraph of feedback (string)
- grammar_mistakes: string listing grammar errors found with corrections (can be multi-line)
- vocabulary_suggestions: string suggesting about 3 stronger academic alternatives (multi-line bullets OK)
""" + SPAN_JSON_RULES_GRADING + """
Keep feedback encouraging but honest. Be accurate — do not inflate scores."""


def _resolve_api_key() -> str:
    return resolve_openai_api_key()


def _post_chat_completions(
    *,
    api_key: str,
    base_url: str,
    organization: str | None,
    project: str | None,
    timeout: float,
    body: dict[str, Any],
) -> dict[str, Any]:
    payload = json.dumps(body, ensure_ascii=False, allow_nan=False)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    if organization:
        headers["OpenAI-Organization"] = organization
    if project:
        headers["OpenAI-Project"] = project
    url = base_url.rstrip("/") + "/chat/completions"
    with httpx.Client(timeout=timeout) as client:
        response = client.post(
            url, headers=headers, content=payload.encode("utf-8")
        )
    if response.status_code != 200:
        raise RuntimeError(
            f"OpenAI API error {response.status_code}: {response.text[:1500]}"
        )
    return response.json()


def _extract_json_text(raw: str) -> str:
    raw = raw.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", raw)
    if fence:
        return fence.group(1).strip()
    return raw


def fetch_openai_json_messages(
    *,
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.35,
    max_completion_tokens: int = 4096,
) -> dict[str, Any]:
    """Run chat completions and parse the assistant message as a JSON object."""
    api_key = _resolve_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = (model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_TIMEOUT", "120"))

    base_body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
    }

    data = None
    last_err: str | None = None
    for use_json_object in (True, False):
        body = dict(base_body)
        if use_json_object:
            body["response_format"] = {"type": "json_object"}
        try:
            data = _post_chat_completions(
                api_key=api_key,
                base_url=base_url,
                organization=org or None,
                project=project or None,
                timeout=timeout,
                body=body,
            )
            break
        except RuntimeError as exc:
            msg = str(exc)
            if use_json_object and "400" in msg:
                last_err = msg
                continue
            raise

    if data is None:
        raise RuntimeError(last_err or "OpenAI request failed.")

    try:
        content = (data["choices"][0]["message"].get("content") or "").strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Bad OpenAI response shape: {exc}") from exc

    content = _extract_json_text(content)
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model did not return valid JSON: {exc}\n{content[:800]}") from exc


def _grade_writing_submission(
    *,
    system_prompt: str,
    question_text: str,
    essay_text: str,
    word_count: int,
    model: str | None = None,
    learner_level: int = 3,
) -> dict[str, Any]:
    full_system = system_prompt + feedback_language_instruction(learner_level)
    user_content = (
        f"Question:\n{question_text}\n\n"
        f"Student response:\n{essay_text}\n\n"
        f"Stated word count: {word_count}\n"
    )

    messages = [
        {"role": "system", "content": full_system},
        {"role": "user", "content": user_content},
    ]

    parsed = fetch_openai_json_messages(messages=messages, model=model)

    return {
        "band_score": _to_float(parsed.get("band_score")),
        "task_achievement_score": _to_float(
            parsed.get("task_achievement") or parsed.get("task_achievement_score")
        ),
        "coherence_score": _to_float(parsed.get("coherence") or parsed.get("coherence_score")),
        "lexical_score": _to_float(parsed.get("lexical") or parsed.get("lexical_score")),
        "grammar_score": _to_float(parsed.get("grammar") or parsed.get("grammar_score")),
        "ai_feedback": str(parsed.get("feedback") or parsed.get("ai_feedback") or "").strip(),
        "grammar_mistakes": str(parsed.get("grammar_mistakes") or "").strip(),
        "vocabulary_suggestions": str(
            parsed.get("vocabulary_suggestions") or ""
        ).strip(),
        "issue_spans": normalize_span_list(parsed.get("issue_spans")),
        "strength_spans": normalize_span_list(parsed.get("strength_spans")),
    }


def grade_task1_response(
    *,
    question_text: str,
    essay_text: str,
    word_count: int,
    model: str | None = None,
    learner_level: int = 3,
) -> dict[str, Any]:
    """IELTS Academic Task 1 — same return shape as Task 2 for Essay model."""
    return _grade_writing_submission(
        system_prompt=GRADING_TASK1_SYSTEM_PROMPT,
        question_text=question_text,
        essay_text=essay_text,
        word_count=word_count,
        model=model,
        learner_level=learner_level,
    )


def grade_task2_essay(
    *,
    question_text: str,
    essay_text: str,
    word_count: int,
    model: str | None = None,
    learner_level: int = 3,
) -> dict[str, Any]:
    """
    Call OpenAI and return a dict with keys matching Essay fields / word-bank parsing.
    Raises RuntimeError on failure.
    """
    return _grade_writing_submission(
        system_prompt=GRADING_SYSTEM_PROMPT,
        question_text=question_text,
        essay_text=essay_text,
        word_count=word_count,
        model=model,
        learner_level=learner_level,
    )


def _to_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def essay_word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text or ""))


def parse_vocabulary_lines(suggestions: str, max_items: int = 5) -> list[str]:
    """Split AI vocabulary block into lines suitable for word bank."""
    if not suggestions:
        return []
    lines = []
    for line in suggestions.replace("\r\n", "\n").split("\n"):
        line = re.sub(r"^\s*[\d\.\)\-•\*]+\s*", "", line.strip())
        if line and len(line) <= 500:
            lines.append(line)
        if len(lines) >= max_items:
            break
    return lines
