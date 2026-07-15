"""Registry for IELTS Academic Reading tests 2–6 (Test 1 stays in academic_test_data.py)."""
from __future__ import annotations

from . import test_2, test_3, test_4, test_5, test_6

TEST_MODULES = {
    2: test_2,
    3: test_3,
    4: test_4,
    5: test_5,
    6: test_6,
}

LIVE_TEST_NUMBERS = (1, 2, 3, 4, 5, 6)

TEST_CATALOG = {
    1: {
        "difficulty_label": "Intermediate",
        "difficulty_class": "intermediate",
        "band_range": "5.0–6.5",
        "diff_note": "Intermediate — suitable for Band 5.0–6.5 learners.",
    },
    2: {
        "difficulty_label": "Standard",
        "difficulty_class": "standard",
        "band_range": "6.0–8.0",
        "diff_note": "Standard · Band 6–8 — realistic academic difficulty with mixed question types.",
    },
    3: {
        "difficulty_label": "Standard",
        "difficulty_class": "standard",
        "band_range": "6.0–8.0",
        "diff_note": "Standard · Band 6–8 — realistic academic difficulty with mixed question types.",
    },
    4: {
        "difficulty_label": "Standard",
        "difficulty_class": "standard",
        "band_range": "6.0–8.0",
        "diff_note": "Standard · Band 6–8 — realistic academic difficulty with mixed question types.",
    },
    5: {
        "difficulty_label": "Standard",
        "difficulty_class": "standard",
        "band_range": "6.0–8.0",
        "diff_note": "Standard · Band 6–8 — realistic academic difficulty with mixed question types.",
    },
    6: {
        "difficulty_label": "Standard",
        "difficulty_class": "standard",
        "band_range": "6.0–8.0",
        "diff_note": "Standard · Band 6–8 — realistic academic difficulty with mixed question types.",
    },
}


def get_test_module(test_number: int):
    return TEST_MODULES.get(test_number)


def get_questions(test_number: int):
    if test_number == 1:
        from reading.academic_test_data import QUESTIONS

        return QUESTIONS
    mod = get_test_module(test_number)
    if not mod:
        return None
    return mod.QUESTIONS


def get_client_payload(test_number: int) -> dict | None:
    if test_number == 1:
        from reading.academic_test_data import get_client_test_payload

        return get_client_test_payload()
    mod = get_test_module(test_number)
    if not mod:
        return None
    return mod.get_payload()
