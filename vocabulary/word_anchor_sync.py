"""Apply curated anchor synonyms from initial_vocab and MANUAL entries."""

from __future__ import annotations

from vocabulary.initial_vocab import INITIAL_WORD_ROWS, ANCHOR_SYNONYMS
from vocabulary.type_it_enrichment import MANUAL
from vocabulary.word_progress_migration import apply_entry_to_word
from vocabulary.models import Word


def anchor_key(topic: str, level: int, word: str) -> tuple[str, int, str]:
    return (topic, int(level), word.strip().lower())


def build_anchor_lookup() -> dict[tuple[str, int, str], dict]:
    lookup: dict[tuple[str, int, str], dict] = {}
    for row in INITIAL_WORD_ROWS:
        word, topic, level, definition, example, collocs, pos, phon = row[:8]
        syns = row[8] if len(row) > 8 else ANCHOR_SYNONYMS.get(word.lower(), [])
        lookup[anchor_key(topic, level, word)] = {
            "definition": definition,
            "example_sentence": example,
            "collocations": list(collocs),
            "part_of_speech": pos,
            "phonetic": phon,
            "synonyms": list(syns),
            "ielts_note": "",
        }
    for (topic, level, word), manual in MANUAL.items():
        key = anchor_key(topic, level, word)
        entry = lookup.get(key, {})
        entry.update(
            {
                "definition": manual.get("definition") or entry.get("definition", ""),
                "example_sentence": manual.get("example") or entry.get("example_sentence", ""),
                "collocations": manual.get("collocations") or entry.get("collocations", []),
                "part_of_speech": manual.get("pos") or entry.get("part_of_speech", ""),
                "ielts_note": manual.get("ielts_note") or entry.get("ielts_note", ""),
                "synonyms": manual.get("synonyms")
                or entry.get("synonyms")
                or ANCHOR_SYNONYMS.get(word, []),
            }
        )
        lookup[key] = entry
    return lookup


ANCHOR_LOOKUP = build_anchor_lookup()


def apply_anchors_to_db(*, topic: str | None = None) -> int:
    n = 0
    qs = Word.objects.all()
    if topic:
        qs = qs.filter(topic=topic)
    for w in qs:
        key = anchor_key(w.topic, w.level, w.word)
        anchor = ANCHOR_LOOKUP.get(key)
        if not anchor:
            continue
        apply_entry_to_word(w, anchor)
        n += 1
    return n
