"""Shared instructions for AI JSON span lists (highlights in learner UI)."""

SPAN_KEYS = frozenset(
    {
        "issue_spans",
        "strength_spans",
        "text_issues",
        "text_strengths",
        "praise_spans",
    }
)

SPAN_JSON_RULES_GRADING = """
Also include these keys (JSON arrays; use [] if nothing to report):
- issue_spans: array of {"excerpt": "substring copied EXACTLY from the student response", "severity": "major" or "minor"}.
  "major" = serious error (grammar, wrong word, unclear meaning) — app shows red.
  "minor" = small slip or weak choice — app shows yellow.
- strength_spans: array of {"excerpt": "substring copied EXACTLY from the student response"} for strong vocabulary, useful collocations, good grammar, or especially clear sentences — app shows green with a star.
Rules: excerpts must match the student text exactly (same spelling, spaces, punctuation). Keep each excerpt short (about 3–80 characters). At most about 12 items per array.
"""

SPAN_JSON_RULES_COACH = """
Also include these keys (JSON arrays; use [] if none):
- issue_spans: array of {"excerpt": "exact substring from the draft being reviewed", "severity": "major" or "minor"} (major=red, minor=yellow in the app).
- strength_spans: array of {"excerpt": "exact substring from that same draft"} for good vocabulary, collocations, grammar, or sentences (green + star in the app).
Match text exactly; short excerpts; max ~12 each.
"""

SPAN_JSON_RULES_PARAPHRASE = """
Also include:
- issue_spans: array of {"excerpt": "exact substring from the STUDENT'S VERSION", "severity": "major" or "minor"} for problems vs the original meaning or language quality.
- strength_spans: array of {"excerpt": "exact substring from the STUDENT'S VERSION"} for well-done paraphrasing, good words, or grammar.
Use [] if none. Match the student's text exactly.
"""


def normalize_span_list(raw: object, max_items: int = 14) -> list[dict]:
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for x in raw:
        if not isinstance(x, dict):
            continue
        ex = str(x.get("excerpt") or x.get("quote") or "").strip()
        if len(ex) < 2:
            continue
        if len(ex) > 400:
            ex = ex[:400]
        item = {"excerpt": ex}
        if "severity" in x:
            item["severity"] = str(x.get("severity") or "major").lower()
        out.append(item)
        if len(out) >= max_items:
            break
    return out
