"""Generate pronunciation MP3s for the Speaking section via OpenAI TTS.

    python manage.py prepare_pronunciation_audio
    python manage.py prepare_pronunciation_audio --force
    python manage.py prepare_pronunciation_audio --word comfortable
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from practice_test.tts import _client, _tts_to_file
from speaking.pronunciation_content import MISPRONOUNCED_WORDS

PRONUNCIATION_VOICE = "nova"
PRONUNCIATION_INSTRUCTIONS = (
    "Speak in clear, natural British English. Pronounce this single English word "
    "accurately at a moderate pace for a language learner preparing for IELTS. "
    "Do not add extra words or sentences."
)


def _out_dir() -> Path:
    return Path(settings.BASE_DIR) / "static" / "pronunciation_audio"


class Command(BaseCommand):
    help = "Generate pronunciation_audio/*.mp3 for each mispronounced word via OpenAI TTS."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
        parser.add_argument("--word", help="Only generate audio for this word (case-insensitive).")

    def handle(self, *args, **opts):
        force = opts["force"]
        word_filter = (opts.get("word") or "").strip().lower()
        out_dir = _out_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

        client = _client()
        made = skipped = 0

        for item in MISPRONOUNCED_WORDS:
            word = item["word"]
            if word_filter and word.lower() != word_filter:
                continue

            dest = out_dir / f"{word.lower()}.mp3"
            if dest.exists() and dest.stat().st_size > 0 and not force:
                self.stdout.write(f"• Skip {dest.name} (exists).")
                skipped += 1
                continue

            self.stdout.write(self.style.MIGRATE_HEADING(f"Generating {dest.name} ({word})…"))
            _tts_to_file(
                client,
                text=word,
                voice=PRONUNCIATION_VOICE,
                instructions=PRONUNCIATION_INSTRUCTIONS,
                out_path=dest,
            )
            self.stdout.write(self.style.SUCCESS(f"  ✓ {dest.name} ({dest.stat().st_size // 1024} KB)"))
            made += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone. Generated {made}, skipped {skipped}."))
