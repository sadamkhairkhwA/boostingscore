"""Scoring helpers — band conversions + OpenAI integration for Writing & Speaking."""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Callable

import httpx

# Reuse the existing key resolver so we never disagree with the rest of the app.
from boostingscore.openai_key import resolve_openai_api_key

logger = logging.getLogger(__name__)


def reading_band_from_correct(correct: int, total: int = 40) -> float:
    """Convert raw correct count to an IELTS Academic Reading band (0.5 steps)."""
    if total <= 0:
        return 0.0
    # IELTS Academic conversion (close approximation).
    bands = [
        (39, 9.0), (37, 8.5), (35, 8.0), (33, 7.5), (30, 7.0),
        (27, 6.5), (23, 6.0), (19, 5.5), (15, 5.0), (13, 4.5),
        (10, 4.0),  (8, 3.5),  (6, 3.0),  (4, 2.5), (0, 0.0),
    ]
    # Scale if total questions differ from 40
    scaled = int(round(correct * 40 / total))
    for threshold, band in bands:
        if scaled >= threshold:
            return float(band)
    return 0.0


def round_half(x: float) -> float:
    return round(x * 2) / 2.0


# ---------- OpenAI client ----------
#
# Connection strategy:
#   1. Default: ignore any HTTP(S)_PROXY env vars (``trust_env=False``).
#      Most personal machines that have those vars set use a local proxy that
#      *blocks* OpenAI — that was the very first networking bug we hit.
#   2. Fallback: honour the env proxy. If the user is on a corporate network
#      or VPN where the proxy is *required*, bypassing it surfaces as
#      ``APIConnectionError: Connection error.`` — exactly what we're seeing
#      from the speaking endpoint right now.
#   ``_call_with_proxy_fallback`` runs an OpenAI call through the primary
#   client first, then transparently retries through the fallback client on
#   any connection-layer failure.

_HTTP_TIMEOUT = httpx.Timeout(120.0, connect=20.0)


def _build_client(*, trust_env: bool, key: str):
    from openai import OpenAI
    return OpenAI(
        api_key=key,
        http_client=httpx.Client(trust_env=trust_env, timeout=_HTTP_TIMEOUT),
        max_retries=3,  # SDK auto-retries transient connection failures
    )


def _client():
    """Primary OpenAI client — ignores system proxies."""
    key = resolve_openai_api_key()
    if not key:
        return None
    try:
        return _build_client(trust_env=False, key=key)
    except Exception:
        logger.exception("Failed to initialise OpenAI client (direct)")
        return None


def _client_via_env_proxy():
    """Fallback OpenAI client — honours HTTP(S)_PROXY env vars."""
    key = resolve_openai_api_key()
    if not key:
        return None
    try:
        return _build_client(trust_env=True, key=key)
    except Exception:
        logger.exception("Failed to initialise OpenAI client (env-proxy)")
        return None


def _format_openai_error(exc: BaseException) -> str:
    """Return a short, debuggable string for an OpenAI / httpx exception.

    Surfaces the *underlying* cause so we can tell apart connection refused,
    DNS failure, SSL handshake error, timeout, etc.
    """
    name = type(exc).__name__
    msg = str(exc) or "no message"
    cause = getattr(exc, "__cause__", None) or getattr(exc, "__context__", None)
    if cause is not None and cause is not exc:
        msg = f"{msg} (caused by {type(cause).__name__}: {cause})"
    return f"{name}: {msg}"


def friendly_openai_error(err: str) -> str:
    """Translate a raw OpenAI exception string (from ``_format_openai_error``)
    into a short, actionable sentence the student can act on.

    The raw string contains the exception class name as a prefix, e.g.
    ``"APIConnectionError: Connection error."`` — we match on that prefix to
    pick the right user-facing message and drop the technical details.
    """
    if not err:
        return ""
    low = err.lower()
    if "apiconnectionerror" in low or "connecterror" in low or "connection error" in low or "name or service not known" in low or "nodename nor servname" in low:
        return ("Couldn't reach OpenAI from this server. Check your internet "
                "connection (and any VPN or proxy) and try again.")
    if "apitimeouterror" in low or "readtimeout" in low or "connecttimeout" in low:
        return "The OpenAI request timed out. Try again in a moment."
    if "authenticationerror" in low or "invalid_api_key" in low or "incorrect api key" in low:
        return ("OpenAI rejected the API key. Update OPENAI_API_KEY in .env "
                "and restart the server, then try again.")
    if "ratelimit" in low or "rate_limit" in low:
        return "OpenAI is rate-limiting requests. Wait a moment and try again."
    if "permission" in low or "forbidden" in low:
        return "OpenAI denied access for this key or model — check your account."
    if "badrequest" in low:
        return "OpenAI rejected the request. Re-record and try again."
    # Fallback — keep the raw line short so it stays readable on results pages.
    return err if len(err) <= 160 else err[:157] + "…"


def _is_connection_error(exc: BaseException) -> bool:
    """True for OpenAI / httpx errors that look like a network problem."""
    try:
        from openai import APIConnectionError, APITimeoutError
    except Exception:  # pragma: no cover — SDK should always be importable
        APIConnectionError = ConnectionError  # type: ignore
        APITimeoutError = TimeoutError  # type: ignore
    if isinstance(exc, (APIConnectionError, APITimeoutError, httpx.HTTPError, ConnectionError, TimeoutError)):
        return True
    return "connection error" in str(exc).lower()


def _call_with_proxy_fallback(call):
    """Execute ``call(client)`` against the primary OpenAI client.

    If the call raises a connection-layer error, retry exactly once through
    the env-proxy client. Returns ``(result, error_string)``: on success
    ``error_string`` is empty; on failure ``result`` is ``None``.
    """
    primary = _client()
    if primary is None:
        return None, "OpenAI API key is not configured on the server."

    try:
        return call(primary), ""
    except Exception as exc:
        if not _is_connection_error(exc):
            logger.exception("OpenAI call failed (non-network) on primary client")
            return None, _format_openai_error(exc)
        logger.warning(
            "OpenAI call hit a connection error on the direct client (%s) — "
            "retrying through the system proxy.",
            _format_openai_error(exc),
        )

    fallback = _client_via_env_proxy()
    if fallback is None:
        return None, "Connection error on direct client and no fallback available."
    try:
        return call(fallback), ""
    except Exception as exc:
        logger.exception("OpenAI call failed on env-proxy fallback client")
        return None, _format_openai_error(exc)


def _empty_writing_feedback(task_kind: str) -> dict[str, Any]:
    return {
        "band_score": 5.0,
        "task_achievement": 5.0 if task_kind == "task1" else None,
        "task_response":    5.0 if task_kind == "task2" else None,
        "coherence_cohesion": 5.0,
        "lexical_resource": 5.0,
        "grammar_accuracy": 5.0,
        "summary": "AI feedback is not available right now — your response was saved.",
        "did_well": [],
        "improve": [],
        "model_answer": "",
        "annotations": [],
        "_no_ai": True,
    }


def _annotate_response(response: str, annotations: list[dict]) -> str:
    """Wrap matched substrings of `response` in coloured HTML spans.

    Each annotation is `{"text": str, "type": "good"|"weak"|"error", "note": str}`.
    Matches are applied in order; only the first occurrence of each `text` is
    wrapped. HTML is escaped before wrapping so user input remains safe.
    """
    import html as _html
    safe = _html.escape(response or "")
    if not isinstance(annotations, list):
        return safe
    css = {"good": "pt-anno pt-anno--good",
           "weak": "pt-anno pt-anno--weak",
           "error":"pt-anno pt-anno--error"}
    for a in annotations:
        if not isinstance(a, dict):
            continue
        text = (a.get("text") or "").strip()
        a_type = (a.get("type") or "").strip().lower()
        klass = css.get(a_type)
        if not text or not klass:
            continue
        needle = _html.escape(text)
        idx = safe.find(needle)
        if idx < 0:
            continue
        note = _html.escape((a.get("note") or "").strip())
        replacement = (
            f'<mark class="{klass}"'
            + (f' title="{note}"' if note else '')
            + f'>{needle}</mark>'
        )
        safe = safe[:idx] + replacement + safe[idx + len(needle):]
    return safe


def score_writing(task_kind: str, prompt: str, response: str, word_count: int) -> dict[str, Any]:
    if not resolve_openai_api_key():
        return _empty_writing_feedback(task_kind)

    criterion_label = "task_achievement" if task_kind == "task1" else "task_response"

    system = (
        "You are a fair, evidence-based IELTS Academic Writing examiner. "
        "Return ONLY valid JSON. Use IELTS half-band scoring (5.0, 5.5, 6.0, …, 9.0). "
        "Be honest but constructive."
    )
    user = (
        f"Task: {task_kind.upper()}\n"
        f"Question / prompt:\n{prompt}\n\n"
        f"Student response ({word_count} words):\n{response}\n\n"
        "Return JSON with this exact shape:\n"
        "{\n"
        '  "band_score": 5.0,\n'
        f'  "{criterion_label}": 5.0,\n'
        '  "coherence_cohesion": 5.0,\n'
        '  "lexical_resource": 5.0,\n'
        '  "grammar_accuracy": 5.0,\n'
        '  "summary": "two-sentence overall feedback",\n'
        '  "did_well": ["...","...","..."],\n'
        '  "improve": ["...","...","..."],\n'
        '  "model_answer": "180-220 word Band 7 model response",\n'
        '  "annotations": [\n'
        '    {"text":"<EXACT verbatim phrase from the student response>", "type":"good|weak|error", "note":"<short reason (max 12 words)>"}\n'
        '  ]\n'
        "}\n\n"
        "Annotations rules:\n"
        "- Use up to 8 annotations total.\n"
        '- "good" = strong vocabulary, accurate complex grammar, well-developed idea.\n'
        '- "weak" = imprecise word choice, repetition, vague linker — not wrong but improvable.\n'
        '- "error" = clear grammar mistake, wrong word, wrong tense, agreement, article, spelling.\n'
        "- Each annotation MUST quote the verbatim phrase exactly as it appears in the student response (case-sensitive, including punctuation). If you can't find an exact phrase to quote, omit that annotation."
    )
    def _call(client):
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

    rsp, err = _call_with_proxy_fallback(_call)
    if err or rsp is None:
        out = _empty_writing_feedback(task_kind)
        out["summary"] = f"AI feedback could not be completed ({err or 'no response'})."
        out["_error"] = err
        return out
    try:
        data = json.loads(rsp.choices[0].message.content or "{}")
    except Exception as exc:
        out = _empty_writing_feedback(task_kind)
        out["summary"] = f"AI returned an invalid response ({type(exc).__name__})."
        out["_error"] = str(exc)
        return out
    # Normalise half-bands
    for k in ("band_score", criterion_label, "coherence_cohesion", "lexical_resource", "grammar_accuracy"):
        if isinstance(data.get(k), (int, float)):
            data[k] = round_half(float(data[k]))
    return data


def transcribe_audio(file_path: str) -> tuple[str, str, dict]:
    """Whisper transcription with verbose_json + word-level timestamps.

    Returns ``(transcript, error, meta)``. ``meta`` carries the raw Whisper
    payload (duration, segments, words) so downstream code can compute
    pauses, words-per-minute and other "every sound"-level metrics. On
    failure ``transcript`` is empty and ``error`` carries a short reason.
    Connection errors automatically retry through the system-proxy fallback.
    """
    if not resolve_openai_api_key():
        return "", "OpenAI API key is not configured on the server.", {}

    def _call(client):
        # Re-open the file inside the call so a retry uses a fresh handle.
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
            )

    rsp, err = _call_with_proxy_fallback(_call)
    if err or rsp is None:
        return "", err or "Whisper returned no response.", {}

    # The SDK returns a model object — normalise to a plain dict so we can
    # store it on SpeakingResponse.raw without serialisation surprises.
    if hasattr(rsp, "model_dump"):
        data = rsp.model_dump()
    elif isinstance(rsp, dict):
        data = rsp
    else:
        data = {"text": str(rsp)}
    text = (data.get("text") or "").strip()
    meta = {
        "duration": data.get("duration"),
        "language": data.get("language"),
        "segments": data.get("segments") or [],
        "words":    data.get("words")    or [],
    }
    return text, "", meta


# Common English speech disfluencies. Whisper sometimes drops these, but
# when it does keep them we can flag them automatically.
_FILLER_PATTERN = re.compile(
    r"\b("
    r"um+|uhm+|uhh*|uh|er+|erm+|ah+|hmm+|mhm+|"  # hesitations
    r"like|y'?know|you\s+know|sort\s+of|kind\s+of|"  # vague hedges
    r"i\s+mean|basically|literally"
    r")\b",
    re.IGNORECASE,
)


def _compute_speaking_metrics(transcript: str, meta: dict, duration_seconds: float) -> dict:
    """Objective speaking metrics computed from the transcript + Whisper timings.

    These don't depend on the AI — they're deterministic facts about the
    recording that we can show alongside the AI band scores.
    """
    words_meta = meta.get("words") or []
    word_count = len(transcript.split()) if transcript else 0

    # Prefer Whisper's reported duration; fall back to client-supplied duration.
    audio_duration = float(meta.get("duration") or duration_seconds or 0.0)
    wpm = (word_count / audio_duration * 60.0) if audio_duration > 0 else 0.0

    # Count rough fillers in the transcript.
    fillers = []
    for m in _FILLER_PATTERN.finditer(transcript or ""):
        fillers.append({"text": m.group(0), "start": m.start(), "end": m.end()})

    # Long pauses: gaps > 1.5s between successive word end / next word start.
    long_pauses: list[dict] = []
    prev_end = None
    for w in words_meta:
        try:
            start = float(w.get("start"))
            end = float(w.get("end"))
        except (TypeError, ValueError):
            continue
        if prev_end is not None and (start - prev_end) > 1.5:
            long_pauses.append({
                "after_word": w.get("word"),
                "from": prev_end,
                "to": start,
                "length": round(start - prev_end, 2),
            })
        prev_end = end

    # Estimate "speaking time" (excluding long pauses) for a fairer WPM if useful.
    return {
        "duration_seconds": round(audio_duration, 2),
        "word_count": word_count,
        "wpm": round(wpm, 1),
        "filler_count": len(fillers),
        "fillers": fillers,
        "long_pause_count": len(long_pauses),
        "long_pauses": long_pauses,
    }


_SPEAKING_ANNO_TYPES = {"good", "weak", "error", "filler", "pronunciation"}


def annotate_speaking_transcript(transcript: str, annotations: list[dict]) -> str:
    """Wrap each annotation's text in a coloured <mark> inside the transcript.

    Same approach as ``_annotate_response`` but with the wider speaking
    annotation types (filler / pronunciation / good / weak / error).
    """
    import html as _html
    safe = _html.escape(transcript or "")
    if not isinstance(annotations, list):
        return safe
    css = {
        "good":          "pt-anno pt-anno--good",
        "weak":          "pt-anno pt-anno--weak",
        "error":         "pt-anno pt-anno--error",
        "filler":        "pt-anno pt-anno--filler",
        "pronunciation": "pt-anno pt-anno--pron",
    }
    for a in annotations:
        if not isinstance(a, dict):
            continue
        text = (a.get("text") or "").strip()
        atype = (a.get("type") or "").strip().lower()
        klass = css.get(atype)
        if not text or not klass:
            continue
        needle = _html.escape(text)
        idx = safe.find(needle)
        if idx < 0:
            continue
        note = _html.escape((a.get("note") or "").strip())
        rep = (
            f'<mark class="{klass}"'
            + (f' title="{note}"' if note else "")
            + f">{needle}</mark>"
        )
        safe = safe[:idx] + rep + safe[idx + len(needle):]
    return safe


def _empty_speaking_criteria() -> dict[str, Any]:
    return {
        c: {"score": 0.0, "notes": "", "did_well": [], "improve": []}
        for c in ("fluency", "vocabulary", "grammar", "pronunciation")
    }


def score_speaking(
    part: int,
    question: str,
    transcript: str,
    duration_seconds: float,
    transcribe_error: str = "",
    metrics: dict | None = None,
) -> dict[str, Any]:
    """Detailed IELTS Speaking scoring.

    Returns four sub-band scores, an overall band, a short overall feedback
    line, **per-criterion breakdowns** (notes + did-well + improve) and
    **inline annotations** that tag specific phrases in the transcript as
    good / weak / error / filler / pronunciation. The objective ``metrics``
    (words per minute, filler count, long pauses) are included verbatim so
    the UI can display them next to the AI commentary.
    """
    metrics = metrics or {}
    if not transcript.strip():
        # Distinguish "couldn't transcribe" from "you didn't say anything".
        if transcribe_error:
            msg = friendly_openai_error(transcribe_error)
        elif duration_seconds < 1.5:
            msg = "Your recording was too short. Please speak for a few seconds and try again."
        else:
            msg = (
                "We could hear audio but no speech was detected. "
                "Check your microphone and try again."
            )
        return {
            "fluency": 0.0, "vocabulary": 0.0, "grammar": 0.0, "pronunciation": 0.0,
            "band": 0.0, "feedback": msg,
            "criteria": _empty_speaking_criteria(),
            "annotations": [],
            "metrics": metrics,
            "_no_transcript": True,
            "_transcribe_error": transcribe_error,
        }
    if not resolve_openai_api_key():
        return {
            "fluency": 6.0, "vocabulary": 6.0, "grammar": 6.0, "pronunciation": 6.0,
            "band": 6.0, "feedback": "AI feedback is not available right now.",
            "criteria": _empty_speaking_criteria(),
            "annotations": [],
            "metrics": metrics,
            "_no_ai": True,
        }

    metrics_summary = (
        f"- Audio length: {metrics.get('duration_seconds', duration_seconds):.1f}s\n"
        f"- Word count: {metrics.get('word_count', len(transcript.split()))}\n"
        f"- Words per minute: {metrics.get('wpm', 0)}\n"
        f"- Filler words detected ({metrics.get('filler_count', 0)}): "
        f"{[f.get('text') for f in (metrics.get('fillers') or [])[:8]]}\n"
        f"- Long pauses >1.5s ({metrics.get('long_pause_count', 0)}): "
        f"{[p.get('length') for p in (metrics.get('long_pauses') or [])[:8]]}"
    )

    system = (
        "You are a strict but fair IELTS Speaking examiner. "
        "Listen carefully to every detail in the transcript — fillers, run-on "
        "sentences, repetition, vocabulary range and accuracy, grammatical "
        "errors, tense mistakes, agreement, articles, collocations, and any "
        "atypical spellings that suggest mispronunciation. "
        "Score on the IELTS 0–9 band scale (half-bands allowed) for Fluency & "
        "Coherence, Lexical Resource, Grammatical Range & Accuracy and "
        "Pronunciation. Return ONLY valid JSON."
    )
    user = (
        f"Speaking Part {part} question:\n{question}\n\n"
        f"Transcript from Whisper (verbatim, including any minor errors):\n"
        f"\"\"\"\n{transcript}\n\"\"\"\n\n"
        f"Objective recording metrics:\n{metrics_summary}\n\n"
        "Return JSON with this EXACT shape:\n"
        "{\n"
        '  "fluency": 6.0,\n'
        '  "vocabulary": 6.0,\n'
        '  "grammar": 6.0,\n'
        '  "pronunciation": 6.0,\n'
        '  "band": 6.0,\n'
        '  "feedback": "2-3 sentence overall summary with one clear next step",\n'
        '  "criteria": {\n'
        '    "fluency":       {"score": 6.0, "notes": "one short sentence", "did_well": ["...","..."], "improve": ["...","..."]},\n'
        '    "vocabulary":    {"score": 6.0, "notes": "one short sentence", "did_well": ["...","..."], "improve": ["...","..."]},\n'
        '    "grammar":       {"score": 6.0, "notes": "one short sentence", "did_well": ["...","..."], "improve": ["...","..."]},\n'
        '    "pronunciation": {"score": 6.0, "notes": "one short sentence", "did_well": ["...","..."], "improve": ["...","..."]}\n'
        "  },\n"
        '  "annotations": [\n'
        '    {"text": "<EXACT verbatim phrase from the transcript>", "type": "good|weak|error|filler|pronunciation", "note": "<short reason, max 12 words>"}\n'
        "  ]\n"
        "}\n\n"
        "Annotation rules:\n"
        "- Quote EXACT verbatim phrases from the transcript (case-sensitive, including punctuation). If you can't find the phrase, omit the annotation.\n"
        "- Use 6 to 14 annotations. Cover every notable strong point AND every notable problem.\n"
        '- "good" = strong word choice, natural collocation, accurate complex grammar.\n'
        '- "weak" = imprecise vocabulary, repetition, vague linker, basic structure.\n'
        '- "error" = clear grammar mistake, wrong tense, agreement, missing article, wrong word.\n'
        '- "filler" = um, uh, like, you know — hesitations, only if present in the transcript.\n'
        '- "pronunciation" = phrase that looks likely mispronounced (atypical spelling, dropped sound).\n\n'
        "Criterion notes rules:\n"
        "- For each criterion, give 2-3 short did_well items AND 2-3 short improve items.\n"
        "- Did_well items should reference specific words/structures the student used.\n"
        "- Improve items should be ACTIONABLE: tell the student exactly what to do next time.\n"
        "- Pronunciation: be cautious — you can only infer from the transcript, fillers and obvious spelling quirks."
    )
    def _call(client):
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

    rsp, err = _call_with_proxy_fallback(_call)
    if err or rsp is None:
        return {
            "fluency": 0.0, "vocabulary": 0.0, "grammar": 0.0, "pronunciation": 0.0,
            "band": 0.0,
            "feedback": friendly_openai_error(err) or "AI scoring failed.",
            "criteria": _empty_speaking_criteria(),
            "annotations": [],
            "metrics": metrics,
            "_error": err,
        }
    try:
        data = json.loads(rsp.choices[0].message.content or "{}")
    except Exception as exc:
        return {
            "fluency": 0.0, "vocabulary": 0.0, "grammar": 0.0, "pronunciation": 0.0,
            "band": 0.0, "feedback": f"AI scoring returned invalid JSON ({type(exc).__name__}).",
            "criteria": _empty_speaking_criteria(),
            "annotations": [],
            "metrics": metrics,
            "_error": str(exc),
        }

    # Normalise band fields to half-steps.
    for k in ("fluency", "vocabulary", "grammar", "pronunciation", "band"):
        v = data.get(k)
        if isinstance(v, (int, float)):
            data[k] = round_half(float(v))
    if not data.get("band"):
        subs = [data.get(k, 0) or 0 for k in ("fluency", "vocabulary", "grammar", "pronunciation")]
        data["band"] = round_half(sum(subs) / 4) if subs else 0.0

    # Make sure the criteria object exists and has the four canonical keys.
    crit = data.get("criteria") or {}
    if not isinstance(crit, dict):
        crit = {}
    for name in ("fluency", "vocabulary", "grammar", "pronunciation"):
        entry = crit.get(name) or {}
        if not isinstance(entry, dict):
            entry = {}
        score = entry.get("score", data.get(name, 0))
        if isinstance(score, (int, float)):
            score = round_half(float(score))
        else:
            score = data.get(name, 0)
        entry["score"] = score
        entry.setdefault("notes", "")
        entry["did_well"] = entry.get("did_well") if isinstance(entry.get("did_well"), list) else []
        entry["improve"]  = entry.get("improve")  if isinstance(entry.get("improve"),  list) else []
        crit[name] = entry
    data["criteria"] = crit

    # Filter annotations to known types.
    annos = data.get("annotations") or []
    if not isinstance(annos, list):
        annos = []
    cleaned = []
    for a in annos:
        if not isinstance(a, dict):
            continue
        if (a.get("type") or "").strip().lower() not in _SPEAKING_ANNO_TYPES:
            continue
        cleaned.append({
            "text": (a.get("text") or "").strip(),
            "type": a["type"].strip().lower(),
            "note": (a.get("note") or "").strip(),
        })
    data["annotations"] = cleaned
    data["metrics"] = metrics
    data.setdefault("feedback", "")
    return data
