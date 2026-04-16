"""Apply safe HTML highlights to student text from AI-returned span lists."""
from __future__ import annotations

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe


def _norm_excerpt(item: dict) -> str:
    if not isinstance(item, dict):
        return ""
    return str(item.get("excerpt") or item.get("quote") or "").strip()


def _issue_class(severity: str) -> str:
    s = (severity or "major").lower()
    if s in ("minor", "low", "medium", "warn", "warning", "yellow"):
        return "hl-issue-minor"
    return "hl-issue-major"


def _find_issue_spans(plain: str, items: list) -> list[tuple[int, int, str, int]]:
    out: list[tuple[int, int, str, int]] = []
    if not plain or not items:
        return out
    for item in items:
        if not isinstance(item, dict):
            continue
        ex = _norm_excerpt(item)
        if len(ex) < 2:
            continue
        c = _issue_class(str(item.get("severity") or "major"))
        start = 0
        while True:
            idx = plain.find(ex, start)
            if idx == -1:
                break
            out.append((idx, idx + len(ex), c, 3))
            start = idx + 1
    return out


def _find_strength_spans(plain: str, items: list) -> list[tuple[int, int, str, int]]:
    out: list[tuple[int, int, str, int]] = []
    if not plain or not items:
        return out
    for item in items:
        if not isinstance(item, dict):
            continue
        ex = _norm_excerpt(item)
        if len(ex) < 2:
            continue
        start = 0
        while True:
            idx = plain.find(ex, start)
            if idx == -1:
                break
            out.append((idx, idx + len(ex), "hl-good", 2))
            start = idx + 1
    return out


def merge_and_render_highlights(plain: str, issue_spans: list | None, strength_spans: list | None) -> SafeString:
    """Non-overlapping highlights: issues beat strengths on overlap; longer spans preferred first within same priority."""
    if not plain:
        return mark_safe("")
    issues = _find_issue_spans(plain, list(issue_spans or []))
    strengths = _find_strength_spans(plain, list(strength_spans or []))
    all_spans = issues + strengths
    # Sort: higher priority first, then earlier start, longer span
    all_spans.sort(key=lambda s: (-s[3], s[0], -(s[1] - s[0])))

    picked: list[tuple[int, int, str]] = []
    for lo, hi, cls, _pr in all_spans:
        if lo >= hi:
            continue
        overlap = False
        for a, b, _ in picked:
            if max(lo, a) < min(hi, b):
                overlap = True
                break
        if not overlap:
            picked.append((lo, hi, cls))

    picked.sort(key=lambda x: x[0])
    parts: list[str] = []
    last = 0
    for lo, hi, cls in picked:
        parts.append(escape(plain[last:lo]))
        parts.append(f'<mark class="{cls}">{escape(plain[lo:hi])}</mark>')
        last = hi
    parts.append(escape(plain[last:]))
    return mark_safe("".join(parts))


def extract_span_lists(meta: dict | None) -> tuple[list, list]:
    if not meta or not isinstance(meta, dict):
        return [], []
    issues = meta.get("issue_spans") or meta.get("text_issues") or []
    strengths = meta.get("strength_spans") or meta.get("praise_spans") or meta.get("text_strengths") or []
    if not isinstance(issues, list):
        issues = []
    if not isinstance(strengths, list):
        strengths = []
    return issues, strengths
