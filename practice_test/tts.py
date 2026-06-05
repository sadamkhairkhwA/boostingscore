"""Generate + cache a single combined IELTS Listening MP3 using OpenAI TTS.

The output is one continuous file (real IELTS-style "plays once"). Each line is
generated separately with its speaker's voice (so dialogues use multiple voices)
and then stitched together with short pauses using pydub, falling back to a
direct ffmpeg concat when pydub cannot decode MP3s without ffprobe.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import httpx
from django.conf import settings
from django.templatetags.static import static

from boostingscore.openai_key import resolve_openai_api_key

from .listening_content import (
    LISTENING_TEST,
    OPENING_NARRATION,
    SECTION_BREAK,
    SPEAK_INSTRUCTIONS,
    VOICES,
)

AUDIO_DIR_NAME = "listening_audio"
AUDIO_FILE_NAME = "main_test.mp3"
BUNDLED_AUDIO_FILE_NAME = "main_test.mp3"

# OpenAI TTS model that supports per-line `instructions` (accent / pace).
TTS_MODEL = "gpt-4o-mini-tts"
# Silent gap inserted between lines when stitching (milliseconds).
PAUSE_BETWEEN_LINES_MS = 600


def bundled_audio_path() -> Path:
    """A pre-generated MP3 committed under static/ for production use.

    Generating listening audio inside a web request is too slow for Railway and
    can trigger "Application failed to respond" 502s. If this file exists, the
    app serves it directly and never calls OpenAI from the Generate button.
    """
    return Path(settings.BASE_DIR) / "static" / AUDIO_DIR_NAME / BUNDLED_AUDIO_FILE_NAME


def audio_dir() -> Path:
    p = Path(settings.MEDIA_ROOT) / AUDIO_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def audio_path() -> Path:
    return audio_dir() / AUDIO_FILE_NAME


def audio_url() -> str:
    if bundled_audio_path().is_file() and bundled_audio_path().stat().st_size > 0:
        return static(f"{AUDIO_DIR_NAME}/{BUNDLED_AUDIO_FILE_NAME}")
    return f"{settings.MEDIA_URL}{AUDIO_DIR_NAME}/{AUDIO_FILE_NAME}"


def audio_exists() -> bool:
    p = audio_path()
    if p.is_file() and p.stat().st_size > 0:
        return True
    bundled = bundled_audio_path()
    return bundled.is_file() and bundled.stat().st_size > 0


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
    """Map a speaker label to an OpenAI voice, defaulting to the narrator."""
    return VOICES.get(speaker.strip().upper(), VOICES["NARRATOR"])


def _tts_to_file(client, *, text: str, voice: str, out_path: Path) -> None:
    """Generate one line and save it as MP3."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Cannot synthesise empty text.")
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=voice,
        input=text,
        instructions=SPEAK_INSTRUCTIONS,
        response_format="mp3",
    ) as response:
        response.stream_to_file(out_path)


def _ffmpeg_exe() -> str:
    """Return a usable ffmpeg executable (system, else imageio-ffmpeg fallback)."""
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


def _configure_pydub_ffmpeg(AudioSegment) -> None:
    """Point pydub at an ffmpeg binary when one is not on PATH."""
    if shutil.which("ffmpeg"):
        return
    AudioSegment.converter = _ffmpeg_exe()


def _concat_file_line(path: Path) -> str:
    safe = str(path.resolve()).replace("'", "'\\''")
    return f"file '{safe}'"


def _stitch_with_ffmpeg(line_files: list[Path], final_path: Path, pause_ms: int) -> None:
    """Fallback stitcher used when pydub cannot decode MP3s without ffprobe."""
    if not line_files:
        raise ValueError("No line files to stitch.")
    ffmpeg = _ffmpeg_exe()
    work_dir = line_files[0].parent
    pause_path = work_dir / "pause.mp3"
    concat_path = work_dir / "concat.txt"

    subprocess.run(
        [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", str(pause_ms / 1000),
            "-q:a", "9", "-acodec", "libmp3lame",
            str(pause_path),
        ],
        check=True,
    )

    lines: list[str] = []
    for i, line_file in enumerate(line_files):
        lines.append(_concat_file_line(line_file))
        if i < len(line_files) - 1:
            lines.append(_concat_file_line(pause_path))
    concat_path.write_text("\n".join(lines) + "\n")

    subprocess.run(
        [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_path),
            "-acodec", "libmp3lame", "-q:a", "2",
            str(final_path),
        ],
        check=True,
    )


def _build_line_plan() -> list[tuple[str, str]]:
    """Flatten the whole test into an ordered list of (speaker, text) lines."""
    plan: list[tuple[str, str]] = [("NARRATOR", OPENING_NARRATION)]
    sections = LISTENING_TEST["sections"]
    for s in sections:
        for speaker, text in s["lines"]:
            plan.append((speaker, text))
        if s["number"] != len(sections):
            plan.append(("NARRATOR", SECTION_BREAK))
    return plan


def generate_audio(verbose: bool = False) -> Path:
    """Generate the full multi-voice listening audio and cache it. Returns the path."""
    client = _client()

    def log(msg: str) -> None:
        if verbose:
            print(f"[listening tts] {msg}")

    plan = _build_line_plan()
    dest = audio_path()

    from pydub import AudioSegment
    _configure_pydub_ffmpeg(AudioSegment)

    with tempfile.TemporaryDirectory(prefix="listening_tts_") as tmp:
        tmp_path = Path(tmp)
        line_files: list[Path] = []

        for i, (speaker, text) in enumerate(plan, start=1):
            voice = _voice_for(speaker)
            line_path = tmp_path / f"line_{i:03d}.mp3"
            log(f"[{i}/{len(plan)}] {speaker} ({voice}): {text[:50]}…")
            _tts_to_file(client, text=text, voice=voice, out_path=line_path)
            line_files.append(line_path)

        log("Stitching lines…")
        try:
            pause = AudioSegment.silent(duration=PAUSE_BETWEEN_LINES_MS)
            combined: AudioSegment | None = None
            for line_path in line_files:
                segment = AudioSegment.from_mp3(line_path)
                combined = segment if combined is None else combined + pause + segment
            if combined is None:
                raise ValueError("Nothing to export.")
            combined.export(dest, format="mp3")
        except (FileNotFoundError, RuntimeError) as exc:
            log(f"pydub stitching unavailable ({exc}); using ffmpeg fallback…")
            _stitch_with_ffmpeg(line_files, dest, PAUSE_BETWEEN_LINES_MS)
        # tmp dir + per-line MP3s are removed automatically on block exit.

    log(f"Wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")
    return dest
