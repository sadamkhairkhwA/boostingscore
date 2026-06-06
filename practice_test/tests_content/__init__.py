"""Per-test content modules for IELTS Practice Tests 2–5.

Each module (test2.py … test5.py) exposes three module-level dicts/lists using
the exact same shapes as Test 1's shipped content:

    READING    -> list of 3 passage dicts (40 questions total)
    LISTENING  -> {"minutes": 30, "sections": [4 section dicts]} (40 questions)
    WRITING    -> {"task1": {...}, "task2": {...}}

Speaking is intentionally left out for now. ``papers.py`` imports these.
"""
