"""Sync IELTS topic tier word lists into ``Word`` rows (used by the topic hub)."""
from __future__ import annotations

from vocabulary.models import Word


def sync_tier_words_to_db(topic: str, tiers: dict[str, list[str]], pack) -> int:
    """Create Word rows for lemmas (placeholders); ties rows to ``pack`` for hub/session filtering."""
    tier_levels = (("beginner", 1), ("standard", 2), ("advanced", 3))
    n = 0
    for tier, level in tier_levels:
        for lemma in tiers.get(tier) or []:
            lemma = (lemma or "").strip()[:100]
            if not lemma:
                continue
            existing = Word.objects.filter(
                topic=topic, word__iexact=lemma, topic_pack=pack
            ).first()
            if existing:
                continue
            Word.objects.create(
                topic=topic,
                word=lemma,
                level=level,
                topic_pack=pack,
                definition=(
                    f"IELTS vocabulary for {tier} level — look up nuance and collocations for “{lemma}”."
                ),
                example_sentence=(
                    f"Example: Writers often discuss how {lemma} connects to wider issues in this topic area."
                ),
                collocations=[],
                part_of_speech="",
                phonetic="",
            )
            n += 1
    return n
