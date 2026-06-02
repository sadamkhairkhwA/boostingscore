"""Generate + cache a single combined IELTS Listening MP3 using OpenAI TTS.

The output is one continuous file (real IELTS-style "plays once") concatenated
from per-section TTS calls. The MP3 frame format from OpenAI's tts-1 is
constant-bitrate, so raw byte concatenation works without an external decoder.
"""

from __future__ import annotations

from pathlib import Path

import httpx
from django.conf import settings

from boostingscore.openai_key import resolve_openai_api_key

from .listening_content import LISTENING_TEST, OPENING_NARRATION, SECTION_BREAK

AUDIO_DIR_NAME = "listening_audio"
AUDIO_FILE_NAME = "main_test.mp3"


def audio_dir() -> Path:
    p = Path(settings.MEDIA_ROOT) / AUDIO_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def audio_path() -> Path:
    return audio_dir() / AUDIO_FILE_NAME


def audio_url() -> str:
    return f"{settings.MEDIA_URL}{AUDIO_DIR_NAME}/{AUDIO_FILE_NAME}"


def audio_exists() -> bool:
    p = audio_path()
    return p.is_file() and p.stat().st_size > 0


def _client():
    key = resolve_openai_api_key()
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set — cannot generate listening audio. "
            "Add it to your .env and try again."
        )
    from openai import OpenAI
    return OpenAI(api_key=key, http_client=httpx.Client(trust_env=False, timeout=120))


def _tts_to_bytes(client, text: str, voice: str) -> bytes:
    """One TTS call → raw MP3 bytes."""
    rsp = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="mp3",
    )
    # The new SDK returns a streamable response with a `.content` (bytes) attr.
    if hasattr(rsp, "content") and isinstance(rsp.content, (bytes, bytearray)):
        return bytes(rsp.content)
    # Older SDKs expose `.read()`
    if hasattr(rsp, "read"):
        return rsp.read()
    # Fallback: iterate
    return b"".join(chunk for chunk in rsp.iter_bytes())  # pragma: no cover


def generate_audio(verbose: bool = False) -> Path:
    """Generate the full listening test audio and cache it. Returns the file path."""
    client = _client()
    voice = LISTENING_TEST.get("voice", "alloy")

    chunks: list[bytes] = []

    def log(msg: str) -> None:
        if verbose:
            print(f"[listening tts] {msg}")

    log("Generating opening narration…")
    chunks.append(_tts_to_bytes(client, OPENING_NARRATION, voice))

    for s in LISTENING_TEST["sections"]:
        log(f"Generating Section {s['number']}: {s['title']!r}…")
        chunks.append(_tts_to_bytes(client, s["script"], voice))
        if s["number"] != len(LISTENING_TEST["sections"]):
            log("Generating inter-section break…")
            chunks.append(_tts_to_bytes(client, SECTION_BREAK, voice))

    dest = audio_path()
    dest.write_bytes(b"".join(chunks))
    log(f"Wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")
    return dest
