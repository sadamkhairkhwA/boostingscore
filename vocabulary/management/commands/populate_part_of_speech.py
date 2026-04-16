import os

from boostingscore.openai_key import resolve_openai_api_key
from django.core.management.base import BaseCommand, CommandError
from openai import OpenAI

from vocabulary.models import Word


ALLOWED = {"noun", "verb", "adjective", "adverb"}


class Command(BaseCommand):
    help = "Populate empty Word.part_of_speech values using OpenAI."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--model",
            default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            help="OpenAI model name to use (default: gpt-4o-mini).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Optional maximum number of words to process (0 = all).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show proposed updates without writing to the database.",
        )

    def handle(self, *args, **options) -> None:
        api_key = resolve_openai_api_key()
        if not api_key:
            raise CommandError(
                "OPENAI_API_KEY is not set. Add it to your environment or .env file."
            )

        model = options["model"]
        limit = max(0, int(options["limit"] or 0))
        dry_run = bool(options["dry_run"])

        org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
        project = os.environ.get("OPENAI_PROJECT")
        client = OpenAI(
            api_key=api_key,
            organization=org or None,
            project=project or None,
        )

        qs = Word.objects.filter(part_of_speech__isnull=True) | Word.objects.filter(
            part_of_speech__exact=""
        )
        qs = qs.order_by("id")
        if limit:
            qs = qs[:limit]

        words = list(qs)
        total = len(words)
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No words need part_of_speech backfill."))
            return

        self.stdout.write(
            self.style.MIGRATE_HEADING(f"Processing {total} word(s) for part_of_speech...")
        )

        updated = 0
        skipped = 0
        failed = 0

        for idx, w in enumerate(words, start=1):
            try:
                pos = self._classify_word(client=client, model=model, word=w.word)
                if pos not in ALLOWED:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"[{idx}/{total}] {w.word}: unexpected POS '{pos}', skipped."
                        )
                    )
                    continue

                if dry_run:
                    self.stdout.write(f"[dry-run {idx}/{total}] {w.word} -> {pos}")
                else:
                    w.part_of_speech = pos
                    w.save(update_fields=["part_of_speech"])
                    self.stdout.write(f"[{idx}/{total}] {w.word} -> {pos}")
                updated += 1
            except Exception as exc:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(f"[{idx}/{total}] {w.word}: failed ({exc})")
                )

        msg = f"Done. updated={updated}, skipped={skipped}, failed={failed}"
        if dry_run:
            msg += " (dry-run)"
        self.stdout.write(self.style.SUCCESS(msg))

    def _classify_word(self, client: OpenAI, model: str, word: str) -> str:
        prompt = (
            f"What is the part of speech of the word '{word}'? "
            "Reply with only one word: noun, verb, adjective, or adverb."
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict classifier. Return exactly one token from: "
                        "noun, verb, adjective, adverb."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        text = (response.choices[0].message.content or "").strip().lower()
        token = text.split()[0] if text else ""
        token = token.strip(".,;:!?'\"()[]{}")
        return token

