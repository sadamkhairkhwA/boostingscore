"""Sync IELTS topic tier word lists into ``Word`` rows (used by the topic hub)."""
from __future__ import annotations

from vocabulary.models import Word
from vocabulary.word_curation import is_placeholder_definition


def placeholder_entry(lemma: str, tier: str) -> dict:
    return {
        "definition": (
            f"IELTS vocabulary for {tier} level — look up nuance and collocations for “{lemma}”."
        ),
        "example_sentence": (
            f"Example: Writers often discuss how {lemma} connects to wider issues in this topic area."
        ),
        "collocations": [],
        "part_of_speech": "",
        "phonetic": "",
        "synonyms": [],
        "ielts_note": "",
    }


def sync_tier_words_to_db(topic: str, tiers: dict[str, list[str]], pack) -> int:
    """Create or update Word rows for lemmas; ties rows to ``pack`` for hub/session filtering."""
    tier_levels = (("beginner", 1), ("standard", 2), ("advanced", 3))
    n = 0
    for tier, level in tier_levels:
        for lemma in tiers.get(tier) or []:
            lemma = (lemma or "").strip()[:100]
            if not lemma:
                continue
            existing = (
                Word.objects.filter(topic=topic, level=level, word__iexact=lemma)
                .order_by("-topic_pack_id", "id")
                .first()
            )
            if existing:
                if not existing.topic_pack_id:
                    existing.topic_pack = pack
                if existing.level != level:
                    existing.level = level
                existing.save(update_fields=["topic_pack", "level"])
                continue
            placeholders = placeholder_entry(lemma, tier)
            Word.objects.create(
                topic=topic,
                word=lemma,
                level=level,
                topic_pack=pack,
                definition=placeholders["definition"],
                example_sentence=placeholders["example_sentence"],
                collocations=placeholders["collocations"],
                part_of_speech=placeholders["part_of_speech"],
                phonetic=placeholders["phonetic"],
                synonyms=placeholders["synonyms"],
                ielts_note=placeholders["ielts_note"],
            )
            n += 1
    return n


def words_needing_enrichment(topic: str | None = None):
    qs = Word.objects.all()
    if topic:
        qs = qs.filter(topic=topic)
    for w in qs.iterator():
        if is_placeholder_definition(w.definition) or not (w.part_of_speech or "").strip():
            yield w
        elif not w.synonyms or len(w.synonyms) < 2:
            yield w
