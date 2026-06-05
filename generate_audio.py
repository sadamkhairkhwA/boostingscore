#!/usr/bin/env python3
"""
Generate IELTS listening test audio with OpenAI TTS.

================================================================================
SETUP (run these once before the first use)
================================================================================

  pip install openai pydub

  brew install ffmpeg
  # pydub needs ffmpeg on your PATH to read/write MP3 files.

  export OPENAI_API_KEY=sk-your-key-here
  # Never commit your key. Set it in the terminal each session, or add it to
  # a local .env file that is listed in .gitignore.

Then generate audio:

  python generate_audio.py

The final MP3 is written to static/listening_audio/ (filename set in OUTPUT below).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# =============================================================================
# CONFIG — edit these, then run: python generate_audio.py
# =============================================================================

# Final file name (saved under static/listening_audio/).
OUTPUT = "test1_s1.mp3"

# Speaker → OpenAI voice name. Change voices here if you like.
VOICES: dict[str, str] = {
    "M": "onyx",        # male
    "W": "nova",        # female
    "NARRATOR": "fable",  # neutral / instructions
}

# How each speaker should sound. This maps a speaker label -> tone instruction
# (passed to gpt-4o-mini-tts as `instructions`). Tweak the wording here to
# change the delivery without touching the code below.
INSTRUCTIONS: dict[str, str] = {
    # Dialogue speakers: natural, like two people chatting on the phone.
    "M": (
        "Speak in a warm, relaxed, conversational British English accent, as if "
        "you are casually chatting with someone on the phone — not reading aloud. "
        "Use a natural everyday pace with light, friendly intonation and natural "
        "rhythm. A little informality is fine; sound like a real person, not a "
        "news reader."
    ),
    "W": (
        "Speak in a warm, relaxed, conversational British English accent, as if "
        "you are casually chatting with someone on the phone — not reading aloud. "
        "Use a natural everyday pace with light, friendly intonation and natural "
        "rhythm. A little informality is fine; sound like a real person, not a "
        "news reader."
    ),
    # Narrator: clear and neutral, but still a natural human voice.
    "NARRATOR": (
        "Speak in a clear, neutral British English accent at a steady, natural "
        "pace. Sound like a calm, human announcer — clear and easy to follow, "
        "but not stiff or robotic."
    ),
}

# Fallback for any speaker without a specific entry above.
DEFAULT_INSTRUCTIONS = INSTRUCTIONS["NARRATOR"]

# Pause between lines in multi-speaker dialogue (milliseconds).
PAUSE_BETWEEN_LINES_MS = 300

# -----------------------------------------------------------------------------
# DIALOGUE SCRIPT — paste your own lines here.
# Each item is (speaker_key, text). speaker_key must exist in VOICES above.
# -----------------------------------------------------------------------------
DIALOGUE_SCRIPT: list[tuple[str, str]] = [
    ("NARRATOR", "Section 1. You will hear a conversation between a student and a librarian."),
    ("NARRATOR", "First, you have some time to look at questions 1 to 5."),
    ("W", "Good morning. How can I help you today?"),
    ("M", "Hello. I'd like to borrow some books for my IELTS preparation."),
    ("W", "Of course. Do you have a library card already?"),
    ("M", "Yes, I registered last week. My name is James Chen."),
    ("W", "Thank you, Mr Chen. You can borrow up to ten items for three weeks."),
    ("NARRATOR", "That is the end of Section 1."),
]


# =============================================================================
# Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "static" / "listening_audio"


def _require_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: OPENAI_API_KEY is not set.\n"
            "  export OPENAI_API_KEY=sk-your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def _tts_to_file(
    client,
    *,
    text: str,
    voice: str,
    out_path: Path,
    instructions: str = DEFAULT_INSTRUCTIONS,
) -> None:
    """Generate one clip and save as MP3."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Cannot synthesise empty text.")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        instructions=instructions,
        response_format="mp3",
    ) as response:
        response.stream_to_file(out_path)


def _configure_pydub_ffmpeg(AudioSegment) -> None:
    """Point pydub at ffmpeg.

    Preferred: a normal system ffmpeg from Homebrew.
    Fallback: imageio-ffmpeg, useful on machines where Homebrew is not installed.
    """
    if shutil.which("ffmpeg"):
        return
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError(
            "ffmpeg was not found. Install it with `brew install ffmpeg`, "
            "or run `pip install imageio-ffmpeg` for the Python fallback."
        ) from exc
    AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()


def _ffmpeg_exe() -> str:
    """Return a usable ffmpeg executable path."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError(
            "ffmpeg was not found. Install it with `brew install ffmpeg`, "
            "or run `pip install imageio-ffmpeg` for the Python fallback."
        ) from exc
    return imageio_ffmpeg.get_ffmpeg_exe()


def _concat_file_line(path: Path) -> str:
    """Format one line for ffmpeg's concat demuxer."""
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
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t",
            str(pause_ms / 1000),
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
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
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-acodec",
            "libmp3lame",
            "-q:a",
            "2",
            str(final_path),
        ],
        check=True,
    )


def generate_dialogue(
    script: list[tuple[str, str]],
    output_filename: str = OUTPUT,
    *,
    voices: dict[str, str] | None = None,
    pause_ms: int = PAUSE_BETWEEN_LINES_MS,
) -> Path:
    """
    Multi-speaker mode: one TTS call per line, then stitch with short pauses.

    script: list of (speaker_key, line) tuples — see DIALOGUE_SCRIPT above.
    """
    from openai import OpenAI
    from pydub import AudioSegment
    _configure_pydub_ffmpeg(AudioSegment)

    voices = voices or VOICES
    api_key = _require_api_key()
    client = OpenAI(api_key=api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    final_path = OUTPUT_DIR / output_filename

    line_files: list[Path] = []
    print(f"Generating {len(script)} lines…")

    with tempfile.TemporaryDirectory(prefix="listening_tts_") as tmp:
        tmp_path = Path(tmp)

        for i, (speaker, line) in enumerate(script, start=1):
            speaker = speaker.strip().upper()
            if speaker not in voices:
                raise KeyError(
                    f"Unknown speaker {speaker!r} on line {i}. "
                    f"Add it to VOICES. Known: {list(voices)}"
                )
            voice = voices[speaker]
            line_path = tmp_path / f"line_{i:03d}.mp3"
            print(f"  [{i}/{len(script)}] {speaker} ({voice}): {line[:50]}…")

            _tts_to_file(
                client,
                text=line,
                voice=voice,
                out_path=line_path,
                instructions=INSTRUCTIONS.get(speaker, DEFAULT_INSTRUCTIONS),
            )
            line_files.append(line_path)

        if not line_files:
            raise ValueError("Script is empty — nothing to export.")

        try:
            combined: AudioSegment | None = None
            pause = AudioSegment.silent(duration=pause_ms)
            for line_path in line_files:
                segment = AudioSegment.from_mp3(line_path)
                combined = segment if combined is None else combined + pause + segment
            if combined is None:
                raise ValueError("Script is empty — nothing to export.")
            combined.export(final_path, format="mp3")
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"pydub stitching unavailable ({exc}); using ffmpeg fallback…")
            _stitch_with_ffmpeg(line_files, final_path, pause_ms)
        # tmp dir and line MP3s are removed automatically when we leave the block.

    print(f"Done → {final_path}")
    return final_path


# =============================================================================
# MONOLOGUE MODE — single voice, one block of text, no stitching
# =============================================================================
#
# Uncomment and call from main(), or run in a separate small script:
#
#   from generate_audio import generate_monologue
#   generate_monologue("Your full monologue text here…", "section4.mp3", voice="fable")
#


def generate_monologue(
    text: str,
    output_filename: str,
    *,
    voice: str = "fable",
    instructions: str = DEFAULT_INSTRUCTIONS,
) -> Path:
    """
    Single-voice mode: pass one block of text → one MP3 file (no line stitching).

    Example:
        generate_monologue(
            "In this lecture I will discuss urban farming…",
            "test1_s4_monologue.mp3",
            voice="fable",
        )
    """
    from openai import OpenAI

    api_key = _require_api_key()
    client = OpenAI(api_key=api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    final_path = OUTPUT_DIR / output_filename

    print(f"Monologue → {final_path} (voice={voice})")
    _tts_to_file(
        client,
        text=text,
        voice=voice,
        out_path=final_path,
        instructions=instructions,
    )
    print(f"Done → {final_path}")
    return final_path


def main() -> None:
    # Default: run the dialogue script defined at the top of this file.
    generate_dialogue(DIALOGUE_SCRIPT, OUTPUT)

    # --- Monologue example (commented out) ---
    # generate_monologue(
    #     "Good morning. Today I will talk about how cities grow their own food…",
    #     "test1_s4_monologue.mp3",
    #     voice="fable",
    # )


if __name__ == "__main__":
    main()
