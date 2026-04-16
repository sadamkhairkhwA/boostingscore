import json
import os
import random
from typing import Any, Dict, List

from boostingscore.openai_key import resolve_openai_api_key
from django.core.management.base import BaseCommand, CommandError

from openai import OpenAI

from vocabulary.models import Word


TOPICS = {
    "Environment": Word.TOPIC_ENVIRONMENT,
    "Health": Word.TOPIC_HEALTH,
    "Technology": Word.TOPIC_TECHNOLOGY,
    "Education": Word.TOPIC_EDUCATION,
    "Society": Word.TOPIC_SOCIETY,
}


SYSTEM_PROMPT = """
You are helping build an IELTS vocabulary trainer.
Given a single topic name, you will return a JSON object with an array
of exactly 40 words for that topic.

The JSON must have this shape:
{
  "words": [
    {
      "word": "string",
      "definition": "string",
      "example_sentence": "string",
      "level": 1 | 2 | 3
    },
    ...
  ]
}

Rules:
- All words must be reasonably advanced but still useful for IELTS.
- Definitions must be concise (1–2 sentences).
- Example sentences must be natural and use the word in context.
- level is an integer: 1 = easier, 2 = medium, 3 = more advanced.
- Never include commentary, markdown, or text outside the JSON object.
""".strip()


class Command(BaseCommand):
    help = "Populate the Word table with 40 words per topic using the OpenAI API."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--model",
            default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            help="OpenAI model name to use (default: gpt-4o-mini).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be created without writing to the database.",
        )

    def handle(self, *args, **options) -> None:
        api_key = resolve_openai_api_key()

        if not api_key:
            raise CommandError(
                "OPENAI_API_KEY is not set. Add it to your environment or .env file."
            )

        model = options["model"]
        dry_run = options["dry_run"]

        org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get(
            "OPENAI_ORG_ID"
        )
        project = os.environ.get("OPENAI_PROJECT")
        client = OpenAI(
            api_key=api_key,
            organization=org or None,
            project=project or None,
        )

        for human_topic, machine_topic in TOPICS.items():
            self.stdout.write(self.style.MIGRATE_HEADING(f"Topic: {human_topic}"))
            existing_count = Word.objects.filter(topic=machine_topic).count()
            if existing_count >= 40:
                self.stdout.write(
                    self.style.NOTICE(
                        f"  Skipping: already have {existing_count} words for this topic."
                    )
                )
                continue

            words = self._generate_words_for_topic(
                client=client, model=model, topic_name=human_topic
            )
            created = 0

            for item in words:
                word_text = item.get("word", "").strip()
                if not word_text:
                    continue

                level = item.get("level")
                if level not in (1, 2, 3):
                    # If the model didn't set a valid level, choose one.
                    level = random.choice((1, 2, 3))

                defaults = {
                    "topic": machine_topic,
                    "level": level,
                    "definition": item.get("definition", "").strip(),
                    "example_sentence": item.get("example_sentence", "").strip(),
                }

                if dry_run:
                    self.stdout.write(f"  [dry-run] {word_text} (L{level})")
                    continue

                obj, created_flag = Word.objects.update_or_create(
                    word=word_text,
                    defaults=defaults,
                )
                if created_flag:
                    created += 1

            if not dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f"  Created {created} new words for {human_topic}.")
                )

    def _generate_words_for_topic(
        self, client: OpenAI, model: str, topic_name: str
    ) -> List[Dict[str, Any]]:
        """
        Ask the OpenAI model for 40 words for the given topic and return
        a list of dicts with keys: word, definition, example_sentence, level.
        """
        user_prompt = (
            "Generate advanced English vocabulary for IELTS related to the topic "
            f"'{topic_name}'. Output MUST be valid JSON only."
        )

        # `responses.create()` in your installed OpenAI client does not support
        # `response_format`, but `chat.completions.create()` does.
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content or ""

        try:
            data = json.loads(text.strip())
        except json.JSONDecodeError as exc:
            raise CommandError(f"Model did not return valid JSON: {exc}\n\n{text}")

        words = data.get("words") or []
        if not isinstance(words, list):
            raise CommandError("JSON must contain a 'words' list.")

        # Truncate or pad to exactly 40 entries if needed.
        if len(words) > 40:
            words = words[:40]

        return words

