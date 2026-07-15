"""Random practice-set selection with per-user cycle tracking."""

from __future__ import annotations

import random

from django.db import transaction

from .models import ListeningTypeCycle
from .models import ListeningPracticeAttempt
from .practice_data import get_sets


def eligible_sets(qtype: str, audio_exists) -> list[dict]:
    """Sets with audio on disk, ready to play."""
    return [
        s for s in get_sets(qtype)
        if audio_exists(s.get("audio", ""))
    ]


def _get_cycle(user, qtype: str) -> ListeningTypeCycle:
    cycle, _ = ListeningTypeCycle.objects.get_or_create(
        student=user,
        question_type=qtype,
        defaults={"completed_set_ids": []},
    )
    return cycle


def cycle_progress(user, qtype: str, audio_exists) -> dict:
    pool = eligible_sets(qtype, audio_exists)
    cycle = _get_cycle(user, qtype)
    completed = len(cycle.completed_set_ids or [])
    total = len(pool)
    remaining = max(0, total - completed)
    return {
        "completed": completed,
        "total": total,
        "remaining": remaining,
        "cycle_number": cycle.cycle_number,
        "pool_empty": total == 0,
    }


def pick_random_set(user, qtype: str, audio_exists) -> dict | None:
    """Return a random set the user has not completed in the current cycle."""
    pool = eligible_sets(qtype, audio_exists)
    if not pool:
        return None

    with transaction.atomic():
        cycle, created = ListeningTypeCycle.objects.select_for_update().get_or_create(
            student=user,
            question_type=qtype,
            defaults={"completed_set_ids": []},
        )

        completed = set(cycle.completed_set_ids or [])
        remaining = [s for s in pool if s["id"] not in completed]

        if not remaining:
            cycle.completed_set_ids = []
            cycle.cycle_number += 1
            cycle.save(update_fields=["completed_set_ids", "cycle_number", "updated_at"])
            remaining = pool[:]

    if len(remaining) > 1:
        last_attempt = (
            ListeningPracticeAttempt.objects.filter(student=user, question_type=qtype)
            .order_by("-created_at")
            .first()
        )
        if last_attempt:
            filtered = [s for s in remaining if s["id"] != last_attempt.set_id]
            if filtered:
                remaining = filtered

    return random.choice(remaining)


def mark_set_completed(user, qtype: str, set_id: str, audio_exists) -> dict:
    """Record a finished test; returns whether the user just finished a full cycle."""
    pool = eligible_sets(qtype, audio_exists)
    pool_size = len(pool)
    if not set_id or pool_size == 0:
        return {"cycle_complete": False, "total": pool_size}

    with transaction.atomic():
        cycle, _ = ListeningTypeCycle.objects.select_for_update().get_or_create(
            student=user,
            question_type=qtype,
            defaults={"completed_set_ids": []},
        )
        ids = list(cycle.completed_set_ids or [])
        if set_id not in ids:
            ids.append(set_id)
            cycle.completed_set_ids = ids
            cycle.save(update_fields=["completed_set_ids", "updated_at"])

    return {
        "cycle_complete": len(ids) >= pool_size,
        "total": pool_size,
    }
