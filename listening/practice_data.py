"""Data for the Listening "Practice by question type" section.

Each question type has 5 practice tests in listening/practice_sets/.
Generate audio: python manage.py prepare_listening_practice_audio --force
"""

QUESTION_TYPES = [
    {
        "slug": "multiple-choice",
        "name": "Multiple choice",
        "blurb": "Pick the correct option (A, B or C) from what you hear.",
    },
    {
        "slug": "gap-fill",
        "name": "Form, note & table completion",
        "blurb": "Fill the gaps in a form, set of notes or table.",
    },
    {
        "slug": "sentence",
        "name": "Sentence completion",
        "blurb": "Complete sentences with words from the recording.",
    },
    {
        "slug": "matching",
        "name": "Matching",
        "blurb": "Match items to a list of options or people.",
    },
    {
        "slug": "map",
        "name": "Map, plan & diagram labelling",
        "blurb": "Label a map or plan using letters from the audio.",
    },
    {
        "slug": "short-answer",
        "name": "Short-answer questions",
        "blurb": "Answer questions in one, two or three words / a number.",
    },
]

TYPE_LABELS = {t["slug"]: t["name"] for t in QUESTION_TYPES}

from listening.practice_sets.gap_fill import TESTS as GAP_FILL_TESTS
from listening.practice_sets.map import TESTS as MAP_TESTS
from listening.practice_sets.map_svgs import MAP_OPTIONS, RIVERSIDE_PARK_MAP_SVG
from listening.practice_sets.matching import TESTS as MATCHING_TESTS
from listening.practice_sets.multiple_choice import TESTS as MULTIPLE_CHOICE_TESTS
from listening.practice_sets.sentence import TESTS as SENTENCE_TESTS
from listening.practice_sets.short_answer import TESTS as SHORT_ANSWER_TESTS

PRACTICE_SETS = {
    "multiple-choice": list(MULTIPLE_CHOICE_TESTS),
    "gap-fill": list(GAP_FILL_TESTS),
    "sentence": list(SENTENCE_TESTS),
    "matching": list(MATCHING_TESTS),
    "map": list(MAP_TESTS),
    "short-answer": list(SHORT_ANSWER_TESTS),
}

TYPE_HUB_SLUGS = frozenset(t["slug"] for t in QUESTION_TYPES)


def get_sets(slug: str) -> list[dict]:
    return list(PRACTICE_SETS.get(slug) or [])


def uses_type_hub(slug: str) -> bool:
    return slug in TYPE_HUB_SLUGS


def get_types():
    """Question types annotated with how many practice sets each has."""
    out = []
    for t in QUESTION_TYPES:
        item = dict(t)
        item["set_count"] = len(PRACTICE_SETS.get(t["slug"], []))
        out.append(item)
    return out


def get_set(slug: str, set_id: str | None = None):
    """Return a practice set for a type slug (first set unless set_id given)."""
    sets = PRACTICE_SETS.get(slug) or []
    if not sets:
        return None
    if set_id:
        for s in sets:
            if s["id"] == set_id:
                return s
        legacy = {
            "mcq-1": "mc-test-1",
            "mcq-2": "mc-test-2",
            "mcq-3": "mc-test-3",
            "mcq-4": "mc-test-4",
            "mcq-5": "mc-test-5",
            "gap-1": "gap-test-1",
            "sentence-1": "sentence-test-1",
            "matching-1": "matching-test-1",
            "map-1": "map-test-1",
            "short-1": "short-test-1",
        }
        mapped = legacy.get(set_id)
        if mapped:
            for s in sets:
                if s["id"] == mapped:
                    return s
    return sets[0]
