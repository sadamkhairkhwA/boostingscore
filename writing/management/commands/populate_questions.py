import json
import os
import re
from typing import Any, Dict, List, Tuple

import httpx
from boostingscore.openai_key import resolve_openai_api_key
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from writing.models import WritingQuestion


TOPICS: List[Tuple[str, str]] = [
    ("Environment", WritingQuestion.TOPIC_ENVIRONMENT),
    ("Health", WritingQuestion.TOPIC_HEALTH),
    ("Technology", WritingQuestion.TOPIC_TECHNOLOGY),
    ("Education", WritingQuestion.TOPIC_EDUCATION),
    ("Society", WritingQuestion.TOPIC_SOCIETY),
]

SYSTEM_PROMPT = """
You create IELTS Writing Task 2 questions for an English learning app.
Respond with a single JSON object only (no markdown fences, no commentary).

Shape:
{
  "questions": [
    {"question_text": "string", "level": 1},
    ...
  ]
}

Rules:
- Exactly 10 objects in "questions".
- Each question_text is a full Task 2 style prompt (opinion / discussion / problem-solution), on the given topic theme.
- level must be 1, 2, or 3. Use roughly 3–4 questions at level 1, 3–4 at level 2, and the rest at level 3 (vary difficulty: level 1 simpler scope, level 3 more abstract).
- All questions must relate clearly to the topic name provided by the user.
""".strip()


def _resolve_api_key() -> str:
    return resolve_openai_api_key()


def _post(api_key: str, base_url: str, org: str | None, project: str | None, timeout: float, body: dict) -> dict:
    payload = json.dumps(body, ensure_ascii=False, allow_nan=False)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    if org:
        headers["OpenAI-Organization"] = org
    if project:
        headers["OpenAI-Project"] = project
    url = base_url.rstrip("/") + "/chat/completions"
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=headers, content=payload.encode("utf-8"))
    if r.status_code != 200:
        raise CommandError(f"OpenAI {r.status_code}: {r.text[:2000]}")
    return r.json()


class Command(BaseCommand):
    help = "Create 10 Task 2 WritingQuestion rows per topic (50 total) via OpenAI."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--model",
            default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing Task 2 questions for each topic before inserting.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
        )

    def handle(self, *args, **options) -> None:
        api_key = _resolve_api_key()
        if not api_key:
            raise CommandError("OPENAI_API_KEY is not set.")

        model = options["model"].strip()
        replace = options["replace"]
        dry_run = options["dry_run"]
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
        project = os.environ.get("OPENAI_PROJECT")
        timeout = float(os.environ.get("OPENAI_TIMEOUT", "120"))

        for human_topic, machine_topic in TOPICS:
            existing = WritingQuestion.objects.filter(
                topic=machine_topic,
                question_type=WritingQuestion.TASK2,
            ).count()
            if existing >= 10 and not replace:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Skip {human_topic}: already {existing} Task 2 questions. Use --replace."
                    )
                )
                continue

            if replace and existing:
                deleted, _ = WritingQuestion.objects.filter(
                    topic=machine_topic,
                    question_type=WritingQuestion.TASK2,
                ).delete()
                self.stdout.write(
                    self.style.WARNING(f"  {human_topic}: deleted {deleted} row(s).")
                )

            user_prompt = (
                f'Generate 10 IELTS Writing Task 2 questions focused on the broad topic: "{human_topic}". '
                "Follow the JSON schema in the system message."
            )

            base_body: Dict[str, Any] = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.5,
                "max_completion_tokens": 8192,
            }

            data = None
            for use_rf in (True, False):
                body = dict(base_body)
                if use_rf:
                    body["response_format"] = {"type": "json_object"}
                try:
                    data = _post(api_key, base_url, org, project, timeout, body)
                    break
                except CommandError as exc:
                    if use_rf and "400" in str(exc):
                        continue
                    raise

            if data is None:
                raise CommandError("OpenAI request failed.")

            try:
                text = (data["choices"][0]["message"].get("content") or "").strip()
            except (KeyError, IndexError, TypeError) as exc:
                raise CommandError(f"Bad response: {exc}")

            fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text)
            if fence:
                text = fence.group(1).strip()

            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                raise CommandError(f"Invalid JSON from model:\n{text[:1200]}")

            items = parsed.get("questions") or []
            if not isinstance(items, list) or len(items) != 10:
                raise CommandError(f"Expected 10 questions for {human_topic}, got {len(items) if isinstance(items, list) else 0}.")

            if dry_run:
                self.stdout.write(f"[dry-run] {human_topic}: {len(items)} questions parsed.")
                continue

            with transaction.atomic():
                for raw in items:
                    qt = (raw.get("question_text") or "").strip()
                    lv = raw.get("level")
                    if not qt:
                        raise CommandError("Empty question_text in batch.")
                    if lv not in (1, 2, 3):
                        lv = 3
                    WritingQuestion.objects.create(
                        question_text=qt,
                        question_type=WritingQuestion.TASK2,
                        topic=machine_topic,
                        level=int(lv),
                    )

            self.stdout.write(
                self.style.SUCCESS(f"Saved 10 Task 2 questions for {human_topic}.")
            )
