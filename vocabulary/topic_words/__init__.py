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


def _split(s: str) -> list[str]:
    return [x.strip() for x in s.replace("\n", " ").split(",") if x.strip()]


def _tier(b: str, s: str, a: str) -> dict[str, list[str]]:
    return {
        "beginner": _split(b),
        "standard": _split(s),
        "advanced": _split(a),
    }


TOPIC_WORDS: dict[str, dict[str, list[str]]] = {
    "environment": _tier(_environment.BEGINNER, _environment.STANDARD, _environment.ADVANCED),
    "health": _tier(_health.BEGINNER, _health.STANDARD, _health.ADVANCED),
    "technology": _tier(_technology.BEGINNER, _technology.STANDARD, _technology.ADVANCED),
    "education": _tier(_education.BEGINNER, _education.STANDARD, _education.ADVANCED),
    "society": _tier(_society.BEGINNER, _society.STANDARD, _society.ADVANCED),
    "travel": _tier(_travel.BEGINNER, _travel.STANDARD, _travel.ADVANCED),
    "science": _tier(_science.BEGINNER, _science.STANDARD, _science.ADVANCED),
    "business": _tier(_business.BEGINNER, _business.STANDARD, _business.ADVANCED),
}
