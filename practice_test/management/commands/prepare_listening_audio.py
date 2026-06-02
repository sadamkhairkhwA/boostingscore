"""Generate the IELTS Listening test MP3 using OpenAI TTS and cache it under MEDIA.

Run once after deployment (or after editing listening_content.py).

    python manage.py prepare_listening_audio
"""

from django.core.management.base import BaseCommand, CommandError

from practice_test import tts


class Command(BaseCommand):
    help = "Generate the IELTS Listening test MP3 using OpenAI TTS."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-generate even if a cached audio file already exists.",
        )

    def handle(self, *args, **opts):
        if tts.audio_exists() and not opts["force"]:
            self.stdout.write(self.style.WARNING(
                f"Audio already exists at {tts.audio_path()} — use --force to regenerate."
            ))
            return
        try:
            path = tts.generate_audio(verbose=True)
        except Exception as exc:
            raise CommandError(f"Audio generation failed: {exc}") from exc
        self.stdout.write(self.style.SUCCESS(f"Wrote {path}"))
