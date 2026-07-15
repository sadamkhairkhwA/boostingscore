"""Generate practice-set MP3s for the Listening learning section via OpenAI TTS.

Reads `lines` from each set in listening.practice_data.PRACTICE_SETS and writes
static/listening_practice/<audio>.mp3 using the same multi-voice pipeline as
the full Practice Tests.

    python manage.py prepare_listening_practice_audio
    python manage.py prepare_listening_practice_audio --force
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from listening.practice_data import PRACTICE_SETS
from practice_test import tts


def _out_dir() -> Path:
    return Path(settings.BASE_DIR) / "static" / "listening_practice"


class Command(BaseCommand):
    help = "Generate listening_practice/*.mp3 from practice_data scripts via OpenAI TTS."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
        parser.add_argument(
            "--type",
            dest="qtype",
            help="Only generate audio for this question-type slug (e.g. multiple-choice).",
        )

    def handle(self, *args, **opts):
        force = opts["force"]
        qtype_filter = opts.get("qtype")
        out_dir = _out_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

        made = skipped = 0
        for slug, sets in PRACTICE_SETS.items():
            if qtype_filter and slug != qtype_filter:
                continue
            for pset in sets:
                audio = pset.get("audio")
                lines = pset.get("lines")
                if not audio or not lines:
                    self.stdout.write(f"• Skip {pset['id']} (no audio/lines).")
                    skipped += 1
                    continue
                dest = out_dir / audio
                if dest.exists() and dest.stat().st_size > 0 and not force:
                    self.stdout.write(f"• Skip {audio} (exists).")
                    skipped += 1
                    continue
                self.stdout.write(self.style.MIGRATE_HEADING(
                    f"Generating {audio} [{slug}] ({len(lines)} lines)…"
                ))
                tts.generate_lines_to_file(lines, dest, verbose=True)
                self.stdout.write(self.style.SUCCESS(f"  ✓ {audio} ({dest.stat().st_size // 1024} KB)"))
                made += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone. Generated {made}, skipped {skipped}."))
