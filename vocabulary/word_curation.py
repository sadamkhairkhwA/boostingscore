"""IELTS vocabulary curation: blocklist, tier targets, and lemma list cleaning."""

from __future__ import annotations

from vocabulary.ielts_replacements import REPLACEMENT_POOLS

TIER_LEVEL = {"beginner": 1, "standard": 2, "advanced": 3}
LEVEL_TIER = {1: "beginner", 2: "standard", 3: "advanced"}

# Standalone A1–B1 lemmas too basic for IELTS study (single words only).
BASIC_WORD_BLOCKLIST = frozenset(
    w.lower()
    for w in """
    happy sad big small house home room bed pen pencil book notebook click type print button
    cable file folder save delete copy paste game television radio headphone mouse keyboard screen
    phone tablet laptop robot machine engine remote speaker microphone photo video camera battery
    charger wifi signal network message call send receive share upload download search password
    app website email error crash virus backup cloud storage memory code program install update
    school teacher student class lesson pen pencil notebook maths letter number question answer
    pass fail graduate playground classroom canteen principal parent certificate diploma campus
    dormitory uniform timetable holiday term sport art history language reading writing study
    group team project talent memory attention effort discipline reward punishment maths
    body arm leg hand foot nose ears eyes teeth throat stomach back breath cough sneeze
    child elderly height weight age pill tablet dose pharmacy nurse wheelchair ambulance
    rain sun snow ice wind air water soil rock wood paper glass rubber plastic metal seed
    leaf root flower fruit fish bird insect mammal reptile human brain cell light heat sound
    earth moon star planet space gravity force motion speed mass temperature electricity magnet
    gas liquid solid animal plant nature lab test fact invention metal glass wood paper rubber
    money bank shop buy sell boss office meeting email phone sign pay receipt spend save loan
    debt stock share brand advertise promote launch start grow expand close succeed partner team
    manager director interview hire fire resign retire promotion job work boss employee salary wage
    family friend neighbour city town village street clothes food rich poor help support protest
    peace war conflict population refugee identity trip vacation flight airport room breakfast
    suitcase bag map tour guide beach mountain countryside weather transport bus train car taxi
    boat ferry bicycle walk road distance time exchange border customs arrival departure check-in
    check-out booking reservation delay cancel lost found visitor local souvenir museum restaurant
    landmark tourist visitor holiday vacation trip travel walk bicycle car taxi bus train boat
    """.split()
)

# Multi-word phrases always kept even if they contain a basic component.
KEEP_COLLOCATIONS = frozenset(
    p.lower()
    for p in """
    fossil fuel mental health social media air pollution water pollution global warming
    carbon footprint greenhouse gas natural disaster food security peer review
    artificial intelligence machine learning climate change renewable energy
    """.split(", ")
)

PLACEHOLDER_PREFIX = "IELTS vocabulary for"


def is_placeholder_definition(defn: str) -> bool:
    return (defn or "").strip().startswith(PLACEHOLDER_PREFIX)


def is_basic_lemma(lemma: str) -> bool:
    """Return True if a standalone lemma should be removed."""
    text = (lemma or "").strip().lower()
    if not text:
        return True
    if text in KEEP_COLLOCATIONS:
        return False
    if " " in text:
        # Multi-word: only block if entire phrase is in blocklist (rare).
        return text in BASIC_WORD_BLOCKLIST
    return text in BASIC_WORD_BLOCKLIST


def _dedupe_preserve_order(lemmas: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for lemma in lemmas:
        key = lemma.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(lemma.strip())
    return out


def curate_tier_list(
    topic: str,
    tier: str,
    lemmas: list[str],
    *,
    target_count: int | None = None,
) -> tuple[list[str], list[str], list[str]]:
    """
    Filter basic words and top up to target_count from replacement pool.

    Returns (curated_list, removed, added).
    """
    target = target_count if target_count is not None else len(lemmas)
    kept: list[str] = []
    removed: list[str] = []
    for lemma in _dedupe_preserve_order(lemmas):
        if is_basic_lemma(lemma):
            removed.append(lemma)
        else:
            kept.append(lemma)

    added: list[str] = []
    existing = {w.lower() for w in kept}
    if len(kept) < target:
        pool = list(REPLACEMENT_POOLS.get(topic, {}).get(tier, []))
        for candidate in pool:
            if len(kept) >= target:
                break
            c = candidate.strip()
            if not c or c.lower() in existing:
                continue
            if is_basic_lemma(c):
                continue
            kept.append(c)
            existing.add(c.lower())
            added.append(c)

    # Global fallback pool if topic pool exhausted.
    if len(kept) < target:
        from vocabulary.ielts_replacements import GLOBAL_REPLACEMENT_POOLS

        for candidate in GLOBAL_REPLACEMENT_POOLS.get(tier, []):
            if len(kept) >= target:
                break
            c = candidate.strip()
            if not c or c.lower() in existing:
                continue
            if is_basic_lemma(c):
                continue
            kept.append(c)
            existing.add(c.lower())
            added.append(c)

    return kept[:target], removed, added


def curate_topic_tiers(
    topic: str,
    tiers: dict[str, list[str]],
) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    """Curate all tiers for one topic. Returns (curated_tiers, report)."""
    curated: dict[str, list[str]] = {}
    report: dict[str, dict[str, list[str]]] = {}
    topic_used: set[str] = set()
    for tier_name in ("beginner", "standard", "advanced"):
        lemmas = tiers.get(tier_name, [])
        target = len(lemmas)
        filtered: list[str] = []
        removed_dup: list[str] = []
        for lemma in lemmas:
            key = lemma.strip().lower()
            if key in topic_used:
                removed_dup.append(lemma)
            else:
                filtered.append(lemma)
        new_list, removed, added = curate_tier_list(
            topic, tier_name, filtered, target_count=target
        )
        final: list[str] = []
        for lemma in new_list:
            key = lemma.strip().lower()
            if key in topic_used:
                continue
            final.append(lemma.strip())
            topic_used.add(key)
        while len(final) < target:
            from vocabulary.ielts_replacements import GLOBAL_REPLACEMENT_POOLS

            pool = list(REPLACEMENT_POOLS.get(topic, {}).get(tier_name, []))
            pool.extend(GLOBAL_REPLACEMENT_POOLS.get(tier_name, []))
            found = False
            for candidate in pool:
                ck = candidate.strip().lower()
                if not ck or ck in topic_used or is_basic_lemma(candidate):
                    continue
                final.append(candidate.strip())
                topic_used.add(ck)
                added.append(candidate.strip())
                found = True
                break
            if not found:
                break
        curated[tier_name] = final[:target]
        report[tier_name] = {"removed": removed + removed_dup, "added": added}
    return curated, report


def curate_all_topic_words(
    raw: dict[str, dict[str, list[str]]],
) -> tuple[dict[str, dict[str, list[str]]], dict]:
    """Curate every topic. Returns (curated_topic_words, full_report)."""
    out: dict[str, dict[str, list[str]]] = {}
    report: dict = {}
    for topic, tiers in raw.items():
        curated, topic_report = curate_topic_tiers(topic, tiers)
        out[topic] = curated
        report[topic] = topic_report
    return out, report


def tier_counts(tiers: dict[str, list[str]]) -> dict[str, int]:
    return {k: len(v) for k, v in tiers.items()}
