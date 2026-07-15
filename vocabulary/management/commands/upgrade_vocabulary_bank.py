"""Upgrade the IELTS vocabulary bank: curation, sync, OpenAI enrichment."""

from __future__ import annotations

import os
from collections import defaultdict

from boostingscore.openai_key import resolve_openai_api_key
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from openai import OpenAI

from vocabulary.ielts_topic_ai import sync_tier_words_to_db, words_needing_enrichment
from vocabulary.models import TopicIELTSWordCache, VocabularyProgress, Word
from vocabulary.topic_words import TOPIC_WORDS, pos_for, write_curated_topic_files
import vocabulary.topic_words as topic_words_pkg
from vocabulary.word_curation import curate_all_topic_words
from vocabulary.word_anchor_sync import apply_anchors_to_db
from vocabulary.word_curation import is_placeholder_definition
from vocabulary.word_enrichment import enrich_batch_openai
from vocabulary.word_progress_migration import (
    apply_entry_to_word,
    attach_legacy_words_to_pack,
    collapse_cross_level_duplicates,
    merge_duplicate_words,
    safe_prune_words,
)


class Command(BaseCommand):
    help = "Curate, sync, and enrich the IELTS vocabulary bank (progress-safe)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--topic", default="", help="Limit to one topic slug")
        parser.add_argument("--batch-size", type=int, default=20)
        parser.add_argument("--skip-openai", action="store_true")
        parser.add_argument("--force-enrich", action="store_true")
        parser.add_argument("--write-topic-files", action="store_true")
        parser.add_argument(
            "--model",
            default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        topic_filter = (options["topic"] or "").strip()
        batch_size = max(5, min(options["batch_size"], 30))
        skip_openai = options["skip_openai"]
        force_enrich = options["force_enrich"]
        model = options["model"]

        topics = [topic_filter] if topic_filter else [t for t, _ in Word.TOPIC_CHOICES]
        if topic_filter and topic_filter not in dict(Word.TOPIC_CHOICES):
            raise CommandError(f"Unknown topic: {topic_filter}")

        curated_words, curation_report = curate_all_topic_words(TOPIC_WORDS)
        total_curated = sum(len(w) for t in curated_words for w in curated_words[t].values())
        self.stdout.write(f"Curated lemma total: {total_curated}")

        progress_before = VocabularyProgress.objects.count()

        if options["write_topic_files"] and not dry:
            write_curated_topic_files(curated_words, topic_words_pkg.__path__[0])
            self.stdout.write("Wrote curated topic_words/*.py")

        dup_stats = merge_duplicate_words(topic=topic_filter or None) if not dry else {}
        if dup_stats:
            self.stdout.write(f"Merged duplicates: {dup_stats}")

        anchor_n = 0 if dry else apply_anchors_to_db(topic=topic_filter or None)
        self.stdout.write(f"Anchor entries applied: {anchor_n}")

        for topic in topics:
            tiers = curated_words.get(topic)
            if not tiers:
                continue
            self.stdout.write(f"Syncing topic: {topic}")
            if dry:
                continue
            obj, _ = TopicIELTSWordCache.objects.update_or_create(
                topic=topic,
                defaults={
                    "status": TopicIELTSWordCache.STATUS_READY,
                    "error_message": "",
                    "beginner": list(tiers["beginner"]),
                    "standard": list(tiers["standard"]),
                    "advanced": list(tiers["advanced"]),
                },
            )
            created = sync_tier_words_to_db(topic, tiers, obj)
            attach_legacy_words_to_pack(topic, obj)
            allowed = {w.strip().lower() for ws in tiers.values() for w in ws if w.strip()}
            prune_stats = safe_prune_words(obj, allowed)
            merge_duplicate_words(topic=topic)
            intended_levels = {
                w.strip().lower(): lvl
                for tier, lvl in (("beginner", 1), ("standard", 2), ("advanced", 3))
                for w in tiers.get(tier, [])
                if w.strip()
            }
            collapse_stats = collapse_cross_level_duplicates(topic, intended_levels)
            self.stdout.write(
                f"  created={created} pruned={prune_stats['deleted']} "
                f"skipped_progress={prune_stats['skipped_with_progress']} "
                f"collapsed={collapse_stats['collapsed']}"
            )

        if not skip_openai and not dry:
            api_key = resolve_openai_api_key()
            if not api_key:
                raise CommandError("OPENAI_API_KEY is not set.")
            client = OpenAI(api_key=api_key)
            pending = []
            for w in words_needing_enrichment(topic_filter or None):
                if not force_enrich and not is_placeholder_definition(w.definition):
                    if w.synonyms and len(w.synonyms) >= 2 and w.part_of_speech:
                        continue
                pending.append(w)
            self.stdout.write(f"Words to enrich via OpenAI: {len(pending)}")
            for i in range(0, len(pending), batch_size):
                batch_words = pending[i : i + batch_size]
                items = [
                    {"word": w.word, "topic": w.topic, "level": w.level} for w in batch_words
                ]
                try:
                    entries = enrich_batch_openai(client, model, items)
                except Exception as exc:
                    self.stderr.write(f"Batch {i // batch_size + 1} failed: {exc}")
                    continue
                by_lemma = {e["word"].strip().lower(): e for e in entries}
                applied = 0
                for w in batch_words:
                    entry = by_lemma.get(w.word.strip().lower())
                    if entry:
                        apply_entry_to_word(w, entry)
                        applied += 1
                self.stdout.write(
                    f"  batch {i // batch_size + 1}: enriched {applied}/{len(batch_words)}"
                )

        if not dry:
            fixed = self._normalise_part_of_speech(topic_filter or None)
            self.stdout.write(f"Part-of-speech normalised on {fixed} words")

        progress_after = VocabularyProgress.objects.count()
        self._print_summary(progress_before, progress_after)

    def _normalise_part_of_speech(self, topic: str | None) -> int:
        """Apply the deterministic curated part of speech so deck ratios are exact."""
        qs = Word.objects.all()
        if topic:
            qs = qs.filter(topic=topic)
        fixed = 0
        for w in qs.iterator():
            pos = pos_for(w.topic, w.word)
            if pos and (w.part_of_speech or "") != pos:
                w.part_of_speech = pos
                w.save(update_fields=["part_of_speech"])
                fixed += 1
        return fixed

    def _print_summary(self, progress_before: int, progress_after: int):
        total = Word.objects.count()
        placeholders = Word.objects.filter(definition__startswith="IELTS vocabulary for").count()
        dupes = (
            Word.objects.values("topic", "level", "word")
            .annotate(n=Count("id"))
            .filter(n__gt=1)
            .count()
        )
        missing_syns = Word.objects.filter(synonyms=[]).count()
        by_topic = {
            row["topic"]: row["n"]
            for row in Word.objects.values("topic").annotate(n=Count("id"))
        }
        self.stdout.write(self.style.SUCCESS("\n=== Vocabulary upgrade summary ==="))
        self.stdout.write(f"Total words: {total}")
        self.stdout.write(f"Placeholder definitions: {placeholders}")
        self.stdout.write(f"Duplicate lemma groups: {dupes}")
        self.stdout.write(f"Words missing synonyms: {missing_syns}")
        self.stdout.write(f"Per topic: {by_topic}")
        self.stdout.write(
            f"VocabularyProgress rows: {progress_before} -> {progress_after}"
        )
        if total < 1400:
            self.stdout.write(self.style.WARNING("Below 1400 word target — run sync for all topics."))
        if placeholders:
            self.stdout.write(self.style.WARNING("Placeholders remain — re-run without --skip-openai."))
        if progress_before != progress_after:
            self.stdout.write(self.style.ERROR("Progress row count changed unexpectedly."))
