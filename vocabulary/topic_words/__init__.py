"""Hardcoded IELTS topic tier word lists (Beginner / Standard / Advanced)."""

from __future__ import annotations

from . import business as _business
from . import education as _education
from . import environment as _environment
from . import health as _health
from . import science as _science
from . import society as _society
from . import technology as _technology
from . import travel as _travel


def _coerce_text(value) -> str:
    if isinstance(value, tuple):
        return " ".join(str(v) for v in value)
    return str(value)


def _split(s) -> list[str]:
    if isinstance(s, tuple):
        return [str(x).strip() for x in s if str(x).strip()]
    text = _coerce_text(s)
    return [x.strip() for x in text.replace("\n", " ").split(",") if x.strip()]


def _tier(b: str, s: str, a: str) -> dict[str, list[str]]:
    return {
        "beginner": _split(b),
        "standard": _split(s),
        "advanced": _split(a),
    }


_TOPIC_MODULES = {
    "environment": _environment,
    "health": _health,
    "technology": _technology,
    "education": _education,
    "society": _society,
    "travel": _travel,
    "science": _science,
    "business": _business,
}


def _dedupe_topic_tiers(tiers: dict[str, list[str]]) -> dict[str, list[str]]:
    """Keep each lemma only in the first tier it appears in (beginner→advanced)."""
    seen: set[str] = set()
    out: dict[str, list[str]] = {"beginner": [], "standard": [], "advanced": []}
    for tier in ("beginner", "standard", "advanced"):
        for lemma in tiers.get(tier, []):
            key = lemma.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            out[tier].append(lemma.strip())
    return out


TOPIC_WORDS: dict[str, dict[str, list[str]]] = {
    topic: _dedupe_topic_tiers(_tier(mod.BEGINNER, mod.STANDARD, mod.ADVANCED))
    for topic, mod in _TOPIC_MODULES.items()
}


# Deterministic part-of-speech map: topic -> lemma(lower) -> pos.
# Priority resolves the few noun/verb homographs (e.g. "transport") to a single pos.
_POS_PRIORITY = (("noun", "NOUNS"), ("verb", "VERBS"), ("adjective", "ADJECTIVES"), ("adverb", "ADVERBS"))


def _build_pos_map() -> dict[str, dict[str, str]]:
    pos_map: dict[str, dict[str, str]] = {}
    for topic, mod in _TOPIC_MODULES.items():
        lemma_pos: dict[str, str] = {}
        for pos, attr in _POS_PRIORITY:
            for lemma in getattr(mod, attr, ()):  # noqa: B009
                key = lemma.strip().lower()
                if key and key not in lemma_pos:
                    lemma_pos[key] = pos
        pos_map[topic] = lemma_pos
    return pos_map


TOPIC_POS_MAP: dict[str, dict[str, str]] = _build_pos_map()


def pos_for(topic: str, lemma: str) -> str | None:
    """Return the curated part of speech for a lemma in a topic, if known."""
    return TOPIC_POS_MAP.get(topic, {}).get((lemma or "").strip().lower())


def write_curated_topic_files(curated: dict[str, dict[str, list[str]]], base_dir) -> None:
    """Rewrite topic_words/*.py BEGINNER/STANDARD/ADVANCED strings from curated lists."""
    import pathlib

    module_map = {
        "environment": "environment",
        "health": "health",
        "technology": "technology",
        "education": "education",
        "society": "society",
        "travel": "travel",
        "science": "science",
        "business": "business",
    }

    def _fmt(words: list[str]) -> str:
        if not words:
            return '("")'
        lines = []
        for w in words:
            safe = w.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'    "{safe}"')
        return "(\n" + ",\n".join(lines) + "\n)"

    for topic, mod_name in module_map.items():
        tiers = curated.get(topic, {})
        path = pathlib.Path(base_dir) / f"{mod_name}.py"
        content = (
            f'BEGINNER = {_fmt(tiers.get("beginner", []))}\n\n'
            f'STANDARD = {_fmt(tiers.get("standard", []))}\n\n'
            f'ADVANCED = {_fmt(tiers.get("advanced", []))}\n'
        )
        path.write_text(content, encoding="utf-8")
