"""Registry of the IELTS Practice Tests (Test 1–5).

Single source of truth for:
  1. which tests appear on the chooser page,
  2. whether each test is ACTIVE (playable) or "coming soon", and
  3. where each test's content lives.

Test 1 uses the shipped content in ``content.py`` + ``listening_content.py``.
Tests 2–5 each live in their own module under ``tests_content/`` (test2.py …
test5.py), exposing READING / LISTENING / WRITING in the exact same shapes.
Speaking is intentionally not included for Tests 2–5 yet.

To take a test offline again, flip its flag in ACTIVE to ``False``.
"""

from __future__ import annotations

# ============================================================================
#  ACTIVATION TOGGLES  —  one line per test (chooser reads this).
# ============================================================================
ACTIVE = {
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
}


# ============================================================================
#  DISPLAY METADATA  —  shown on the chooser cards.
#  (No difficulty/band labels: real IELTS papers are all the same level.)
# ============================================================================
TEST_META = {
    1: {"title": "Practice Test 1",
        "blurb": "Urban farming, sleep & memory, coral reefs — a full four-section paper."},
    2: {"title": "Practice Test 2",
        "blurb": "The science of tea, biomimicry and decision-making, plus listening & writing."},
    3: {"title": "Practice Test 3",
        "blurb": "Cartography, monarch migration and the economics of happiness."},
    4: {"title": "Practice Test 4",
        "blurb": "Taste & flavour, Roman roads and AI in medicine."},
    5: {"title": "Practice Test 5",
        "blurb": "Early agriculture, the physics of bridges and memory champions."},
}


# ============================================================================
#  PUBLIC HELPERS
# ============================================================================

def is_active(n: int) -> bool:
    return bool(ACTIVE.get(n, False))


def list_tests() -> list[dict]:
    """Return chooser-ready metadata for all five tests, in order."""
    return [
        {
            "number": n,
            "active": is_active(n),
            "title": TEST_META[n]["title"],
            "blurb": TEST_META[n]["blurb"],
        }
        for n in sorted(TEST_META)
    ]


def get_content(n: int) -> dict | None:
    """Return a test's content bundle: reading / writing / listening (+ speaking).

    Test 1 pulls from the shipped modules; Tests 2–5 from their own module.
    Speaking is only present for Test 1 (Tests 2–5 add it later).
    """
    if n == 1:
        from . import content as C
        from . import listening_content as LC
        return {
            "reading": C.READING_PASSAGES,
            "writing": C.WRITING_TASKS,
            "listening": LC.LISTENING_TEST,
            "speaking": C.SPEAKING_PARTS,
        }
    if n in (2, 3, 4, 5):
        from importlib import import_module
        mod = import_module(f"practice_test.tests_content.test{n}")
        return {
            "reading": mod.READING,
            "writing": mod.WRITING,
            "listening": mod.LISTENING,
            "speaking": None,
        }
    return None
