"""Progress-safe helpers when upgrading the vocabulary bank."""

from __future__ import annotations

from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from vocabulary.models import TypeItAttempt, TypeItResult, VocabularyProgress, Word


def word_has_progress(word: Word) -> bool:
    if VocabularyProgress.objects.filter(word=word).exists():
        return True
    if TypeItAttempt.objects.filter(word=word).exists():
        return True
    if TypeItResult.objects.filter(word=word).exists():
        return True
    return False


def _merge_progress_fields(dst: VocabularyProgress, src: VocabularyProgress) -> None:
    dst.mastery_level = max(dst.mastery_level or 1, src.mastery_level or 1)
    dst.times_marked_hard = (dst.times_marked_hard or 0) + (src.times_marked_hard or 0)
    dst.easy_chip_master_count = max(
        dst.easy_chip_master_count or 0, src.easy_chip_master_count or 0
    )
    dst.is_hard_word = dst.is_hard_word or src.is_hard_word
    dst.is_favored = dst.is_favored or src.is_favored
    if src.next_review and (not dst.next_review or src.next_review < dst.next_review):
        dst.next_review = src.next_review
    if src.last_reviewed and (
        not dst.last_reviewed or src.last_reviewed > dst.last_reviewed
    ):
        dst.last_reviewed = src.last_reviewed


def reassign_progress_to_word(from_word: Word, to_word: Word) -> None:
    """Move user progress/attempts from one Word row to another."""
    for prog in VocabularyProgress.objects.filter(word=from_word).select_related("student"):
        existing = VocabularyProgress.objects.filter(student=prog.student, word=to_word).first()
        if existing:
            _merge_progress_fields(existing, prog)
            existing.save()
            prog.delete()
        else:
            prog.word = to_word
            prog.save(update_fields=["word"])

    TypeItAttempt.objects.filter(word=from_word).update(word=to_word)
    TypeItResult.objects.filter(word=from_word).update(word=to_word)


def pick_canonical_word(words: list[Word]) -> Word:
    """Prefer pack-linked row; otherwise lowest id."""
    pack_rows = [w for w in words if w.topic_pack_id]
    if pack_rows:
        return min(pack_rows, key=lambda w: w.id)
    return min(words, key=lambda w: w.id)


def merge_duplicate_words(*, topic: str | None = None) -> dict:
    """
    Merge duplicate (topic, level, word) rows.
    Returns stats dict.
    """
    stats = {"groups": 0, "merged": 0, "deleted": 0}
    qs = Word.objects.all()
    if topic:
        qs = qs.filter(topic=topic)

    dup_keys = (
        qs.values("topic", "level", "word")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    )
    for row in dup_keys:
        group = list(
            qs.filter(
                topic=row["topic"],
                level=row["level"],
                word__iexact=row["word"],
            ).order_by("id")
        )
        if len(group) < 2:
            continue
        stats["groups"] += 1
        canonical = pick_canonical_word(group)
        for other in group:
            if other.id == canonical.id:
                continue
            reassign_progress_to_word(other, canonical)
            other.delete()
            stats["deleted"] += 1
            stats["merged"] += 1
    return stats


def replace_word_in_place(word: Word, *, new_lemma: str, entry: dict) -> Word:
    """Update a Word row in place (preserves primary key and progress)."""
    word.word = new_lemma[:100]
    word.definition = entry.get("definition", word.definition)
    word.example_sentence = entry.get("example_sentence", word.example_sentence)
    word.part_of_speech = (entry.get("part_of_speech") or word.part_of_speech or "")[:50]
    word.collocations = entry.get("collocations") or word.collocations or []
    word.synonyms = entry.get("synonyms") or word.synonyms or []
    word.ielts_note = entry.get("ielts_note") or word.ielts_note or ""
    word.phonetic = (entry.get("phonetic") or word.phonetic or "")[:100]
    word.save()
    return word


def apply_entry_to_word(word: Word, entry: dict) -> Word:
    """Apply enriched fields to an existing Word without changing lemma."""
    word.definition = entry.get("definition", word.definition)
    word.example_sentence = entry.get("example_sentence", word.example_sentence)
    word.part_of_speech = (entry.get("part_of_speech") or word.part_of_speech or "")[:50]
    word.collocations = entry.get("collocations") or word.collocations or []
    word.synonyms = entry.get("synonyms") or word.synonyms or []
    word.ielts_note = entry.get("ielts_note") or word.ielts_note or ""
    word.phonetic = (entry.get("phonetic") or word.phonetic or "")[:100]
    word.save()
    return word


@transaction.atomic
def safe_delete_word(word: Word) -> bool:
    """Delete only when no user progress exists."""
    if word_has_progress(word):
        return False
    word.delete()
    return True


@transaction.atomic
def safe_prune_words(pack, allowed_lemmas: set[str]) -> dict:
    """
    Remove pack words not in allowed set.
    Words with progress are kept (not deleted).
    """
    stats = {"deleted": 0, "skipped_with_progress": 0}
    allowed = {w.strip().lower() for w in allowed_lemmas if w.strip()}
    for w in Word.objects.filter(topic_pack=pack):
        if w.word.strip().lower() in allowed:
            continue
        if word_has_progress(w):
            stats["skipped_with_progress"] += 1
            continue
        w.delete()
        stats["deleted"] += 1
    return stats


@transaction.atomic
def collapse_cross_level_duplicates(topic: str, intended_levels: dict[str, int]) -> dict:
    """
    Collapse rows sharing a lemma across levels into one row at the intended level.

    Keeps a row that already has real (non-placeholder) content when possible,
    resets its level to the tier-assigned level, moves progress off the others,
    then deletes the duplicates. Progress is never lost.
    """
    from vocabulary.word_curation import is_placeholder_definition

    stats = {"collapsed": 0, "deleted": 0}
    groups: dict[str, list[Word]] = {}
    for w in Word.objects.filter(topic=topic):
        groups.setdefault(w.word.strip().lower(), []).append(w)

    for lemma, rows in groups.items():
        if len(rows) < 2:
            continue
        target_level = intended_levels.get(lemma)
        # Prefer a content-rich row; otherwise one already at the target level.
        rich = [r for r in rows if not is_placeholder_definition(r.definition)]
        if rich:
            canonical = min(rich, key=lambda r: r.id)
        elif target_level is not None:
            at_target = [r for r in rows if r.level == target_level]
            canonical = min(at_target or rows, key=lambda r: r.id)
        else:
            canonical = min(rows, key=lambda r: r.id)

        if target_level is not None and canonical.level != target_level:
            canonical.level = target_level
            canonical.save(update_fields=["level"])

        for other in rows:
            if other.id == canonical.id:
                continue
            reassign_progress_to_word(other, canonical)
            other.delete()
            stats["deleted"] += 1
        stats["collapsed"] += 1
    return stats


@transaction.atomic
def attach_legacy_words_to_pack(topic: str, pack) -> dict:
    """
    Link legacy (no pack) rows to pack when lemma matches; merge duplicates.
    """
    stats = {"attached": 0, "merged": 0}
    pack_lemmas = {
        w.word.strip().lower(): w
        for w in Word.objects.filter(topic_pack=pack)
    }
    legacy = Word.objects.filter(topic=topic, topic_pack__isnull=True)
    for leg in legacy:
        key = leg.word.strip().lower()
        if key in pack_lemmas:
            canonical = pack_lemmas[key]
            reassign_progress_to_word(leg, canonical)
            leg.delete()
            stats["merged"] += 1
        else:
            leg.topic_pack = pack
            leg.save(update_fields=["topic_pack"])
            pack_lemmas[key] = leg
            stats["attached"] += 1
    return stats
