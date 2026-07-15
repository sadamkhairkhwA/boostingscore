"""Spaced-repetition reminders for study sections beyond vocabulary flashcards."""
from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

# section_slug -> (label, url_name, default_interval_days)
REVIEW_SECTIONS = {
    "vocabulary": ("Vocabulary flashcards", "vocabulary:home", 1),
    "reading_vocab_context": ("Reading vocabulary in context", "reading:vocab_context", 3),
    "reading_timed_drill": ("Reading timed drill", "reading:timed_drill_index", 7),
    "listening_notes": ("Listening note-taking", "listening:section4_notes", 3),
    "listening_details": ("Listening numbers & dates", "listening:detail_drills", 1),
    "writing_grammar": ("Writing grammar checklist", "writing:grammar_mistakes", 7),
    "speaking_record": ("Speaking practice recording", "speaking:home", 3),
}

INTERVAL_LADDER = [1, 3, 7, 14, 30]


def _get_profile(user: User):
    from vocabulary.models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def mark_section_reviewed(user: User, section_slug: str) -> None:
    """Record completion and schedule next review using interval ladder."""
    if section_slug not in REVIEW_SECTIONS:
        return
    profile = _get_profile(user)
    reviews = dict(profile.section_reviews or {})
    entry = dict(reviews.get(section_slug) or {})
    count = int(entry.get("review_count") or 0) + 1
    idx = min(count - 1, len(INTERVAL_LADDER) - 1)
    days = INTERVAL_LADDER[idx]
    now = timezone.now()
    entry.update(
        {
            "last_reviewed": now.isoformat(),
            "next_review": (now + timedelta(days=days)).isoformat(),
            "review_count": count,
            "interval_days": days,
        }
    )
    reviews[section_slug] = entry
    profile.section_reviews = reviews
    profile.save(update_fields=["section_reviews"])


def get_due_review_items(user: User, vocab_due_count: int = 0) -> list[dict]:
    """Items due for spaced review (vocab + other sections)."""
    now = timezone.now()
    items = []

    if vocab_due_count > 0:
        items.append(
            {
                "slug": "vocabulary",
                "label": "Vocabulary flashcards",
                "detail": f"{vocab_due_count} word{'s' if vocab_due_count != 1 else ''} due",
                "url_name": "vocabulary:home",
                "priority": 1,
            }
        )

    profile = _get_profile(user)
    reviews = profile.section_reviews or {}
    for slug, (label, url_name, default_days) in REVIEW_SECTIONS.items():
        if slug == "vocabulary":
            continue
        entry = reviews.get(slug) or {}
        next_iso = entry.get("next_review")
        if not next_iso:
            continue
        try:
            from django.utils.dateparse import parse_datetime

            next_dt = parse_datetime(next_iso)
            if next_dt and timezone.is_naive(next_dt):
                next_dt = timezone.make_aware(next_dt)
        except Exception:
            continue
        if next_dt and next_dt <= now:
            days_over = (now - next_dt).days
            items.append(
                {
                    "slug": slug,
                    "label": label,
                    "detail": f"Due for review ({days_over}d overdue)" if days_over else "Due for review today",
                    "url_name": url_name,
                    "priority": 2,
                }
            )

    items.sort(key=lambda x: x["priority"])
    return items
