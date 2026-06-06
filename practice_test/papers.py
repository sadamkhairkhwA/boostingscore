"""Registry of the IELTS Practice Tests (Test 1–5).

This is the single place that controls:
  1. which tests appear on the chooser page,
  2. whether each test is ACTIVE (playable) or "coming soon", and
  3. where each test's content lives.

Test 1 already works and uses the shipped content in ``content.py`` and
``listening_content.py`` — it is NOT edited here.

Tests 2–5 are scaffolded below with clearly-labelled, empty content blocks.
To bring a test online:
  1. Paste your content into that test's block (reading / writing / listening /
     speaking) further down this file.
  2. Drop the four listening audio files into ``static/listening_audio/``
     using the names listed in that test's ``listening["audio"]``.
  3. Flip the test's flag in ACTIVE below to ``True``  ← the only toggle needed.
"""

from __future__ import annotations

# ============================================================================
#  ACTIVATION TOGGLES  —  flip a test to True once its content is ready.
#  (This is the one-line-per-test switch the chooser page reads.)
# ============================================================================
ACTIVE = {
    1: True,    # Test 1 — live
    2: False,   # Test 2 — coming soon
    3: False,   # Test 3 — coming soon
    4: False,   # Test 4 — coming soon
    5: False,   # Test 5 — coming soon
}


# ============================================================================
#  DISPLAY METADATA  —  shown on the chooser cards.
# ============================================================================
TEST_META = {
    1: {
        "title": "Practice Test 1",
        "blurb": "Urban farming, sleep & memory, coral reefs. A balanced first mock.",
        "difficulty": "Intermediate",
        "band_range": "5.0 – 7.5",
    },
    2: {
        "title": "Practice Test 2",
        "blurb": "Second full mock — Reading, Writing, Listening, Speaking.",
        "difficulty": "Intermediate",
        "band_range": "5.0 – 7.5",
    },
    3: {
        "title": "Practice Test 3",
        "blurb": "Third full mock — Reading, Writing, Listening, Speaking.",
        "difficulty": "Upper-Intermediate",
        "band_range": "5.5 – 7.5",
    },
    4: {
        "title": "Practice Test 4",
        "blurb": "Fourth full mock — Reading, Writing, Listening, Speaking.",
        "difficulty": "Upper-Intermediate",
        "band_range": "5.5 – 8.0",
    },
    5: {
        "title": "Practice Test 5",
        "blurb": "Fifth full mock — Reading, Writing, Listening, Speaking.",
        "difficulty": "Advanced",
        "band_range": "6.5 – 8.5",
    },
}


# ============================================================================
#  CONTENT BLOCKS FOR TESTS 2–5
#
#  Each block mirrors the shape of Test 1's content. Reference shapes:
#
#   READING passage:
#     {"number": 1, "title": "...", "paragraphs": ["...", "..."],
#      "questions": [
#         {"type": "tfng", "id": "t2r1q1", "text": "...", "answer": "TRUE"},
#         {"type": "gap",  "id": "t2r1q6", "text": "... ____ ...", "answer": "word"},
#         {"type": "mcq",  "id": "t2r1q9", "text": "...",
#          "options": ["A", "B", "C", "D"], "answer": "A"},
#      ]}
#
#   WRITING: {"task1": {"kind":"task1","title":"Writing — Task 1","minutes":20,
#                       "min_words":150,"instructions":"...","chart_svg":"<svg…>"},
#             "task2": {"kind":"task2","title":"Writing — Task 2","minutes":40,
#                       "min_words":250,"instructions":"..."}}
#
#   LISTENING section:
#     {"number": 1, "title": "Section 1 — ...",
#      "instructions": "Questions 1–10. ...",
#      "audio": "test2_s1.mp3",          # file in static/listening_audio/
#      "questions": [
#         {"type":"form","id":"t2l1q1","text":"...","answer":"40"},
#         {"type":"mcq","id":"t2l1q4","text":"...","options":[...],"answer":"..."},
#         {"type":"short","id":"t2l1q8","text":"...","answer_keywords":[...]},
#      ]}
#
#   SPEAKING part:
#     {"part": 1, "title": "Part 1 — ...", "minutes": 5, "intro": "...",
#      "questions": ["...", "..."]}
# ============================================================================

def _empty_paper(n: int) -> dict:
    """A blank, correctly-shaped content scaffold for test number ``n``."""
    return {
        # ---------------- READING (paste 3 passages, 40 questions total) -----
        "reading": [
            # {"number": 1, "title": "", "paragraphs": [], "questions": []},
            # {"number": 2, "title": "", "paragraphs": [], "questions": []},
            # {"number": 3, "title": "", "paragraphs": [], "questions": []},
        ],
        # ---------------- WRITING (Task 1 + Task 2) --------------------------
        "writing": {
            "task1": {
                "kind": "task1", "title": "Writing — Task 1",
                "minutes": 20, "min_words": 150,
                "instructions": "",   # paste the Task 1 prompt
                "chart_svg": "",      # paste an inline <svg> chart (optional)
            },
            "task2": {
                "kind": "task2", "title": "Writing — Task 2",
                "minutes": 40, "min_words": 250,
                "instructions": "",   # paste the Task 2 essay prompt
            },
        },
        # ---------------- LISTENING (4 sections, 40 questions) ---------------
        # Audio files expected in static/listening_audio/ with these names:
        "listening": {
            "minutes": 30,
            "sections": [
                {"number": 1, "title": "Section 1 — ", "instructions": "",
                 "audio": f"test{n}_s1.mp3", "questions": []},
                {"number": 2, "title": "Section 2 — ", "instructions": "",
                 "audio": f"test{n}_s2.mp3", "questions": []},
                {"number": 3, "title": "Section 3 — ", "instructions": "",
                 "audio": f"test{n}_s3.mp3", "questions": []},
                {"number": 4, "title": "Section 4 — ", "instructions": "",
                 "audio": f"test{n}_s4.mp3", "questions": []},
            ],
        },
        # ---------------- SPEAKING (3 parts) ---------------------------------
        "speaking": [
            {"part": 1, "title": "Part 1 — Introduction and interview",
             "minutes": 5, "intro": "", "questions": []},
            {"part": 2, "title": "Part 2 — The long turn (cue card)",
             "minutes": 4, "intro": "", "prep_seconds": 60, "questions": []},
            {"part": 3, "title": "Part 3 — Two-way discussion",
             "minutes": 5, "intro": "", "questions": []},
        ],
    }


# Each test 2–5 starts from a blank scaffold. Paste content directly into the
# returned dicts below (e.g. TEST_CONTENT[2]["reading"].append({...})) or edit
# _empty_paper for a shared default. They stay "coming soon" until ACTIVE[n].
TEST_CONTENT = {
    2: _empty_paper(2),
    3: _empty_paper(3),
    4: _empty_paper(4),
    5: _empty_paper(5),
}


# ============================================================================
#  PUBLIC HELPERS
# ============================================================================

def is_active(n: int) -> bool:
    return bool(ACTIVE.get(n, False))


def list_tests() -> list[dict]:
    """Return chooser-ready metadata for all five tests, in order."""
    out = []
    for n in sorted(TEST_META):
        meta = TEST_META[n]
        out.append({
            "number": n,
            "active": is_active(n),
            "title": meta["title"],
            "blurb": meta["blurb"],
            "difficulty": meta["difficulty"],
            "band_range": meta["band_range"],
        })
    return out


def get_content(n: int) -> dict | None:
    """Return a test's content bundle (Test 1 pulls from the shipped modules)."""
    if n == 1:
        from . import content as C
        from . import listening_content as LC
        return {
            "reading": C.READING_PASSAGES,
            "writing": C.WRITING_TASKS,
            "listening": LC.LISTENING_TEST,
            "speaking": C.SPEAKING_PARTS,
        }
    return TEST_CONTENT.get(n)
