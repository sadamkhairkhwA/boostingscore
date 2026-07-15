"""Print a per-topic vocabulary upgrade report (removed/added/PoS mix/samples)."""

from __future__ import annotations

import json
from collections import Counter

from django.core.management.base import BaseCommand

from vocabulary.models import Word

_NOUN = {"noun", "noun phrase"}


def _bucket(pos: str) -> str:
    p = (pos or "").strip().lower()
    if p in _NOUN or p.endswith("noun"):
        return "noun"
    if p == "verb":
        return "verb"
    if p == "adjective":
        return "adjective"
    if p == "adverb":
        return "adverb"
    return "phrase"


class Command(BaseCommand):
    help = "Report vocabulary changes per topic against a before-snapshot JSON."

    def add_arguments(self, parser):
        parser.add_argument("--before", default="/tmp/vocab_snapshot_before.json")
        parser.add_argument("--samples", type=int, default=10)

    def handle(self, *args, **options):
        samples = options["samples"]
        try:
            before = json.load(open(options["before"], encoding="utf-8"))
        except (OSError, ValueError):
            before = {}

        topics = [t for t, _ in Word.TOPIC_CHOICES]
        grand = Counter()
        grand_removed = grand_added = 0

        for topic in topics:
            before_set = {w.strip().lower() for w in before.get(topic, [])}
            rows = list(Word.objects.filter(topic=topic))
            after_set = {r.word.strip().lower() for r in rows}
            removed = sorted(before_set - after_set)
            added = sorted(after_set - before_set)
            grand_removed += len(removed)
            grand_added += len(added)

            pos_counts = Counter(_bucket(r.part_of_speech) for r in rows)
            for k, v in pos_counts.items():
                grand[k] += v
            total = len(rows) or 1

            self.stdout.write(self.style.SUCCESS(f"\n=== {topic.upper()} ==="))
            self.stdout.write(
                f"before={len(before_set)} after={len(rows)} "
                f"removed={len(removed)} added={len(added)}"
            )
            self.stdout.write(
                "PoS mix: "
                + "  ".join(
                    f"{k} {pos_counts.get(k,0)} ({100*pos_counts.get(k,0)/total:.0f}%)"
                    for k in ("noun", "verb", "adjective", "adverb", "phrase")
                )
            )
            if removed:
                self.stdout.write("removed sample: " + ", ".join(removed[:15]))
            if added:
                self.stdout.write("added sample: " + ", ".join(added[:15]))
            sample_rows = list(
                Word.objects.filter(topic=topic).order_by("level", "word")[:samples]
            )
            self.stdout.write("samples:")
            for r in sample_rows:
                self.stdout.write(
                    f"  - {r.word} [{r.part_of_speech}] (L{r.level}) "
                    f"syn={', '.join(r.synonyms[:3]) if r.synonyms else '—'}"
                )

        gtot = sum(grand.values()) or 1
        self.stdout.write(self.style.SUCCESS("\n=== OVERALL ==="))
        self.stdout.write(f"total words: {gtot}")
        self.stdout.write(f"removed: {grand_removed}  added: {grand_added}")
        self.stdout.write(
            "PoS mix: "
            + "  ".join(
                f"{k} {grand.get(k,0)} ({100*grand.get(k,0)/gtot:.1f}%)"
                for k in ("noun", "verb", "adjective", "adverb", "phrase")
            )
        )
