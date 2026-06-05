"""Generate + cache a single combined IELTS Listening MP3 using OpenAI TTS.

Each line is generated separately with its speaker's voice (so dialogues use
multiple natural British voices) and then stitched together with short, varied
pauses. The final mix is loudness-normalised for consistent volume, and a small
JSON of section start-times is written alongside the audio so the player can
auto-scroll/highlight the current section.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import httpx
from django.conf import settings
from django.templatetags.static import static

from boostingscore.openai_key import resolve_openai_api_key

from .listening_content import (
    DEFAULT_INSTRUCTIONS,
    INSTRUCTIONS,
    LISTENING_TEST,
    OPENING_NARRATION,
    SECTION_BREAK,
    VOICES,
)

AUDIO_DIR_NAME = "listening_audio"
AUDIO_FILE_NAME = "main_test.mp3"
BUNDLED_AUDIO_FILE_NAME = "main_test.mp3"
TIMING_FILE_NAME = "main_test.timing.json"

TTS_MODEL = "gpt-4o-mini-tts"
PAUSE_LINE_MS = 320       # natural gap between consecutive lines
PAUSE_SECTION_MS = 800    # longer gap around a section break


# --------------------------------------------------------------------------- #
# Paths / URLs
# --------------------------------------------------------------------------- #

def bundled_audio_path() -> Path:
    return Path(settings.BASE_DIR) / "static" / AUDIO_DIR_NAME / BUNDLED_AUDIO_FILE_NAME


def bundled_timing_path() -> Path:
    return Path(settings.BASE_DIR) / "static" / AUDIO_DIR_NAME / TIMING_FILE_NAME


def audio_dir() -> Path:
    p = Path(settings.MEDIA_ROOT) / AUDIO_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def audio_path() -> Path:
    return audio_dir() / AUDIO_FILE_NAME


def timing_path() -> Path:
    return audio_dir() / TIMING_FILE_NAME


def _bundled_ok() -> bool:
    p = bundled_audio_path()
    return p.is_file() and p.stat().st_size > 0


def audio_url() -> str:
    if _bundled_ok():
        return static(f"{AUDIO_DIR_NAME}/{BUNDLED_AUDIO_FILE_NAME}")
    return f"{settings.MEDIA_URL}{AUDIO_DIR_NAME}/{AUDIO_FILE_NAME}"


def audio_exists() -> bool:
    p = audio_path()
    if p.is_file() and p.stat().st_size > 0:
        return True
    return _bundled_ok()


def audio_timing() -> list[dict]:
    """Return [{'number': n, 'start': seconds}, ...] for the active audio, or []."""
    for p in (bundled_timing_path() if _bundled_ok() else timing_path(), timing_path()):
        try:
            if p.is_file():
                return json.loads(p.read_text())
        except Exception:
            continue
    return []


# --------------------------------------------------------------------------- #
# OpenAI + ffmpeg helpers
# --------------------------------------------------------------------------- #

def _client():
    key = resolve_openai_api_key()
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set — cannot generate listening audio. "
            "Add it to your .env and try again."
        )
    from openai import OpenAI
    return OpenAI(api_key=key, http_client=httpx.Client(trust_env=False, timeout=120))


def _voice_for(speaker: str) -> str:
    return VOICES.get(speaker.strip().upper(), VOICES["NARRATOR"])


def _instructions_for(speaker: str) -> str:
    return INSTRUCTIONS.get(speaker.strip().upper(), DEFAULT_INSTRUCTIONS)


def _tts_to_file(client, *, text: str, voice: str, instructions: str, out_path: Path) -> None:
    text = (text or "").strip()
    if not text:
        raise ValueError("Cannot synthesise empty text.")
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=voice,
        input=text,
        instructions=instructions,
        response_format="mp3",
    ) as response:
        response.stream_to_file(out_path)


def _ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "ffmpeg was not found. Install it with `brew install ffmpeg`, "
            "or run `pip install imageio-ffmpeg` for the Python fallback."
        ) from exc
    return imageio_ffmpeg.get_ffmpeg_exe()


def _mp3_duration(path: Path) -> float:
    """Best-effort duration in seconds via ffmpeg's stderr banner."""
    out = subprocess.run([_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", out)
    if not m:
        return 0.0
    h, mm, ss = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mm * 60 + ss


def _make_silence(ffmpeg: str, out_path: Path, ms: int) -> None:
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-f", "lavfi",
         "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
         "-t", str(ms / 1000), "-q:a", "9", "-acodec", "libmp3lame", str(out_path)],
        check=True,
    )


def _concat_line(path: Path) -> str:
    return "file '%s'" % str(path.resolve()).replace("'", "'\\''")


# --------------------------------------------------------------------------- #
# Build plan + generate
# --------------------------------------------------------------------------- #

def _build_plan() -> list[dict]:
    """Ordered lines with the section each belongs to and the pause that follows."""
    plan: list[dict] = [{"speaker": "NARRATOR", "text": OPENING_NARRATION, "section": 0, "pause": PAUSE_SECTION_MS}]
    sections = LISTENING_TEST["sections"]
    for s in sections:
        lines = s["lines"]
        for i, (speaker, text) in enumerate(lines):
            plan.append({
                "speaker": speaker, "text": text, "section": s["number"],
                "pause": PAUSE_LINE_MS,
            })
        if s["number"] != len(sections):
            plan.append({"speaker": "NARRATOR", "text": SECTION_BREAK, "section": 0, "pause": PAUSE_SECTION_MS})
    return plan


def _compute_timing(plan: list[dict], durations: list[float]) -> list[dict]:
    """Section-number -> first-line start time (seconds)."""
    timing: list[dict] = []
    seen: set[int] = set()
    t = 0.0
    for item, dur in zip(plan, durations):
        sec = item["section"]
        if sec and sec not in seen:
            seen.add(sec)
            timing.append({"number": sec, "start": round(t, 2)})
        t += dur + item["pause"] / 1000.0
    return sorted(timing, key=lambda x: x["number"])


def generate_audio(verbose: bool = False) -> Path:
    """Generate the full multi-voice listening audio + timing. Returns the path."""
    client = _client()
    ffmpeg = _ffmpeg_exe()

    def log(msg: str) -> None:
        if verbose:
            print(f"[listening tts] {msg}")

    plan = _build_plan()
    dest = audio_path()
    durations: list[float] = []

    with tempfile.TemporaryDirectory(prefix="listening_tts_") as tmp:
        tmp_path = Path(tmp)
        line_files: list[Path] = []

        for i, item in enumerate(plan, start=1):
            voice = _voice_for(item["speaker"])
            line_path = tmp_path / f"line_{i:03d}.mp3"
            log(f"[{i}/{len(plan)}] S{item['section']} {item['speaker']} ({voice}): {item['text'][:48]}…")
            _tts_to_file(
                client, text=item["text"], voice=voice,
                instructions=_instructions_for(item["speaker"]), out_path=line_path,
            )
            durations.append(_mp3_duration(line_path))
            line_files.append(line_path)

        # Silence clips for the two pause lengths.
        pause_files = {}
        for ms in {PAUSE_LINE_MS, PAUSE_SECTION_MS}:
            pf = tmp_path / f"pause_{ms}.mp3"
            _make_silence(ffmpeg, pf, ms)
            pause_files[ms] = pf

        # Build concat list (line, pause, line, pause, ...).
        concat_lines: list[str] = []
        for idx, lf in enumerate(line_files):
            concat_lines.append(_concat_line(lf))
            if idx < len(line_files) - 1:
                concat_lines.append(_concat_line(pause_files[plan[idx]["pause"]]))
        concat_path = tmp_path / "concat.txt"
        concat_path.write_text("\n".join(concat_lines) + "\n")

        # Final encode with EBU R128 loudness normalisation (consistent volume).
        log("Stitching + mastering (loudnorm)…")
        subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(concat_path),
             "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-acodec", "libmp3lame", "-q:a", "2", str(dest)],
            check=True,
        )

    timing = _compute_timing(plan, durations)
    timing_path().write_text(json.dumps(timing))
    log(f"Wrote {dest} ({dest.stat().st_size / 1024:.1f} KB); timing: {timing}")
    return dest
