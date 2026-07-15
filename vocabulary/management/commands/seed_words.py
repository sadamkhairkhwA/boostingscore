from django.core.management.base import BaseCommand

from vocabulary.initial_vocab import INITIAL_WORD_ROWS, bulk_create_words
from vocabulary.models import Word


class Command(BaseCommand):
    help = (
        "Load bundled IELTS-style vocabulary (same list as the initial data "
        "migration). Idempotent: existing (topic, level, word) rows are skipped."
    )

    def handle(self, *args, **options):
        try:
            created, skipped = bulk_create_words(Word, skip_if_exists=True)
        except Exception as exc:
            # Release/startup must not take down the app if the bank is incomplete.
            self.stderr.write(self.style.ERROR(f"seed_words failed (non-fatal): {exc}"))
            return
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created} words, skipped {skipped} (already present). "
                f"Total rows in bundle: {len(INITIAL_WORD_ROWS)}."
            )
        )
