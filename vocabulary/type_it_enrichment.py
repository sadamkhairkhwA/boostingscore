"""
Hardcoded IELTS-style fields for Type it practice (merged onto Word rows for JSON payloads).
Key: (topic, level, word lowercased).
"""
from __future__ import annotations

from typing import Any

from vocabulary.models import Word as WordModel

_VALID_TOPICS = {c[0] for c in WordModel.TOPIC_CHOICES}

# Full manual entries — used when present; otherwise DB Word fields + generic note.
MANUAL: dict[tuple[str, int, str], dict[str, Any]] = {
    (
        "environment",
        1,
        "climate",
    ): {
        "definition": (
            "The general weather conditions in a particular area or region, "
            "or long-term patterns of temperature, rainfall, and wind on Earth."
        ),
        "example": (
            "The rapid melting of polar ice sheets is contributing to rising sea levels, "
            "posing a significant threat to coastal communities worldwide."
        ),
        "collocations": [
            "climate change",
            "climate crisis",
            "changing climate",
            "tackle climate change",
            "global climate",
        ],
        "ielts_note": (
            "Very frequent in Task 2 environment questions. Pair with verbs like "
            "tackle, address, and mitigate; avoid vague phrases without evidence."
        ),
        "pos": "noun",
    },
    (
        "environment",
        1,
        "pollution",
    ): {
        "definition": (
            "Harmful or poisonous substances introduced into air, water, or soil, "
            "often as a result of human activity."
        ),
        "example": (
            "Industrial pollution has contaminated rivers in several developing regions, "
            "forcing authorities to introduce stricter emission controls."
        ),
        "collocations": [
            "air pollution",
            "water pollution",
            "reduce pollution",
            "plastic pollution",
            "combat pollution",
        ],
        "ielts_note": (
            "Often contrasted with economic growth in IELTS essays. Use specific types "
            "(air, noise, plastic) rather than only the noun alone."
        ),
        "pos": "noun",
    },
    (
        "environment",
        1,
        "habitat",
    ): {
        "definition": (
            "The natural home or environment where a plant or animal normally lives "
            "and finds food, shelter, and breeding conditions."
        ),
        "example": (
            "Urban expansion has destroyed large areas of wildlife habitat, leaving "
            "several species struggling to find sufficient territory."
        ),
        "collocations": [
            "natural habitat",
            "wildlife habitat",
            "loss of habitat",
            "protect habitats",
            "marine habitat",
        ],
        "ielts_note": (
            "Common in biodiversity and urbanisation essays. Collocates strongly with "
            "loss, destruction, and protection."
        ),
        "pos": "noun",
    },
    (
        "environment",
        1,
        "drought",
    ): {
        "definition": (
            "A long period when there is little or no rain, causing water shortages "
            "and serious problems for farming and people."
        ),
        "example": (
            "Severe drought forced farmers to reduce crop yields, pushing food prices "
            "higher in several regions."
        ),
        "collocations": [
            "severe drought",
            "prolonged drought",
            "drought conditions",
            "face drought",
            "climate-related drought",
        ],
        "ielts_note": (
            "Useful for cause–effect essays linking climate change to agriculture and "
            "food security."
        ),
        "pos": "noun",
    },
    (
        "environment",
        1,
        "fossil fuel",
    ): {
        "definition": (
            "Coal, oil, or natural gas formed from ancient organic matter; burning these "
            "releases carbon dioxide and other greenhouse gases."
        ),
        "example": (
            "Many governments still rely heavily on fossil fuels, although investment "
            "in renewables is gradually increasing."
        ),
        "collocations": [
            "burn fossil fuels",
            "phase out fossil fuels",
            "dependence on fossil fuels",
            "fossil fuel industry",
        ],
        "ielts_note": (
            "Central to energy and climate arguments. Often appears in problem–solution "
            "essays about energy policy."
        ),
        "pos": "noun phrase",
    },
    (
        "environment",
        1,
        "recycle",
    ): {
        "definition": (
            "To treat used materials so that they can be used again to make new products, "
            "rather than throwing them away as waste."
        ),
        "example": (
            "Households that recycle paper and glass can significantly reduce the volume "
            "of waste sent to landfill."
        ),
        "collocations": [
            "recycle waste",
            "recycle materials",
            "recycling scheme",
            "recycle plastic",
        ],
        "ielts_note": (
            "Frequent in individual-action vs government-responsibility questions. "
            "Combine with reduce and reuse for a stronger band."
        ),
        "pos": "verb",
    },
    (
        "environment",
        1,
        "deforestation",
    ): {
        "definition": (
            "The clearing of large areas of forest, usually so that the land can be used "
            "for farming, logging, or development."
        ),
        "example": (
            "Deforestation in tropical regions has accelerated carbon emissions and "
            "threatened biodiversity hotspots."
        ),
        "collocations": [
            "tackle deforestation",
            "rates of deforestation",
            "tropical deforestation",
            "combat deforestation",
        ],
        "ielts_note": (
            "Often linked to agriculture and logging. Good for cause–effect and "
            "two-part environment questions."
        ),
        "pos": "noun",
    },
    (
        "environment",
        1,
        "conservation",
    ): {
        "definition": (
            "The protection of plants, animals, and natural places from damage or loss; "
            "the careful use of natural resources."
        ),
        "example": (
            "National parks play a vital role in the conservation of endangered species "
            "and fragile ecosystems."
        ),
        "collocations": [
            "wildlife conservation",
            "energy conservation",
            "conservation efforts",
            "nature conservation",
        ],
        "ielts_note": (
            "Often compared with economic development. Use precise verbs: support, "
            "fund, and prioritise conservation."
        ),
        "pos": "noun",
    },
}


def _generic_note(topic: str, level: int, pos: str) -> str:
    topic_title = topic.replace("_", " ").title()
    band_hint = {1: "Band 5–6", 2: "Band 6–7", 3: "Band 7+"}.get(level, "Band 6+")
    return (
        f"In IELTS Writing Task 2, this {pos or 'word'} often appears in {topic_title.lower()} "
        f"essays. Show range by using strong collocations and clear stance — typical of {band_hint} responses."
    )


def merge_word_payload(word_obj, manual: dict[str, Any] | None) -> dict[str, Any]:
    """Build client payload for one Word (model instance)."""
    m = manual or {}
    definition = (m.get("definition") or word_obj.definition or "").strip()
    example = (m.get("example") or word_obj.example_sentence or "").strip()
    collocations = m.get("collocations")
    if not collocations:
        c = word_obj.collocations
        collocations = c if isinstance(c, list) else []
    pos = (m.get("pos") or word_obj.part_of_speech or "word").strip()
    ielts_note = (m.get("ielts_note") or getattr(word_obj, "ielts_note", None) or "").strip()
    if not ielts_note:
        ielts_note = _generic_note(word_obj.topic, word_obj.level, pos)
    synonyms = m.get("synonyms")
    if not synonyms:
        syns = getattr(word_obj, "synonyms", None)
        synonyms = syns if isinstance(syns, list) else []
    return {
        "id": word_obj.id,
        "word": word_obj.word,
        "definition": definition,
        "example": example,
        "collocations": collocations[:8],
        "synonyms": synonyms[:3],
        "ielts_note": ielts_note,
        "pos": pos,
        "topic": word_obj.topic,
        "topic_label": word_obj.get_topic_display(),
        "level": word_obj.level,
        "level_label": word_obj.get_level_display(),
    }


def manual_key(word) -> tuple[str, int, str]:
    return (word.topic, int(word.level), word.word.strip().lower())


def enrich_word(word) -> dict[str, Any]:
    mk = manual_key(word)
    manual = MANUAL.get(mk)
    return merge_word_payload(word, manual)


# Optional fixed order per deck slug (otherwise alphabetical by word).
DECK_WORD_ORDER: dict[str, list[str]] = {
    "environment-1": [
        "climate",
        "pollution",
        "habitat",
        "drought",
        "fossil fuel",
        "recycle",
        "deforestation",
        "conservation",
    ],
}


def ordered_words_for_deck(slug: str, topic: str, level: int):
    """Return Word queryset order for deck (list of Word instances)."""
    order = DECK_WORD_ORDER.get(slug.strip().lower())
    words: list[WordModel] = []
    if order:
        for w in order:
            o = WordModel.objects.filter(
                topic=topic, level=level, word__iexact=w
            ).first()
            if o:
                words.append(o)
        return words
    return list(
        WordModel.objects.filter(topic=topic, level=level).order_by("word")
    )


def parse_deck_slug(deck_id: str) -> tuple[str, int]:
    """Parse `topic-level` e.g. environment-1 → ('environment', 1)."""
    deck_id = (deck_id or "").strip().lower()
    if "-" not in deck_id:
        raise ValueError("invalid")
    topic, _, level_s = deck_id.rpartition("-")
    if not topic or not level_s.isdigit():
        raise ValueError("invalid")
    level = int(level_s)
    if level not in (1, 2, 3):
        raise ValueError("invalid")
    if topic not in _VALID_TOPICS:
        raise ValueError("invalid")
    return topic, level


def deck_title(topic: str, level: int) -> str:
    tl = dict(WordModel.TOPIC_CHOICES).get(topic, topic.title())
    ll = dict(WordModel.LEVEL_CHOICES).get(level, str(level))
    return f"{tl} · {ll}"
