"""Generate the multi-voice Listening MP3s for Practice Tests 2-5 via OpenAI TTS.

Produces static/listening_audio/testN_sX.mp3 from the speaker-tagged scripts in
``practice_test.tests_content.listening_scripts`` using the same pipeline as
Test 1 (per-line voices, natural pauses, EBU R128 loudness normalisation).

Examples:
    python manage.py prepare_test_listening_audio                # all tests/sections
    python manage.py prepare_test_listening_audio --test 3       # only Test 3
    python manage.py prepare_test_listening_audio --test 4 --section 2
    python manage.py prepare_test_listening_audio --force        # overwrite existing
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from practice_test import tts
from practice_test.tests_content.listening_scripts import SCRIPTS

TESTS = (2, 3, 4, 5)
SECTIONS = (1, 2, 3, 4)


def _static_audio_dir() -> Path:
    """Where Test 1's bundled audio lives (static/listening_audio/)."""
    return Path(settings.BASE_DIR) / "static" / "listening_audio"


class Command(BaseCommand):
    help = "Generate listening audio (testN_sX.mp3) for Practice Tests 2-5 via OpenAI TTS."

    def add_arguments(self, parser):
        parser.add_argument("--test", type=int, choices=TESTS, help="Only this test number.")
        parser.add_argument("--section", type=int, choices=SECTIONS, help="Only this section number.")
        parser.add_argument("--force", action="store_true", help="Regenerate even if the file exists.")

    def handle(self, *args, **opts):
        tests = [opts["test"]] if opts.get("test") else list(TESTS)
        sections = [opts["section"]] if opts.get("section") else list(SECTIONS)
        force = opts["force"]

        out_dir = _static_audio_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

        targets = [(t, s) for t in tests for s in sections]
        made, skipped = 0, 0

        for test_n, sec_n in targets:
            lines = SCRIPTS.get((test_n, sec_n))
            if not lines:
                raise CommandError(f"No script defined for Test {test_n} Section {sec_n}.")

            dest = out_dir / f"test{test_n}_s{sec_n}.mp3"
            if dest.exists() and dest.stat().st_size > 0 and not force:
                self.stdout.write(f"• Skip test{test_n}_s{sec_n}.mp3 (exists; use --force).")
                skipped += 1
                continue

            self.stdout.write(self.style.MIGRATE_HEADING(
                f"Generating test{test_n}_s{sec_n}.mp3 ({len(lines)} lines)…"
            ))
            tts.generate_lines_to_file(lines, dest, verbose=True)
            kb = dest.stat().st_size / 1024
            self.stdout.write(self.style.SUCCESS(f"  ✓ {dest.name} ({kb:.0f} KB)"))
            made += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone. Generated {made}, skipped {skipped}."))
        self.stdout.write(f"Files in: {out_dir}")
