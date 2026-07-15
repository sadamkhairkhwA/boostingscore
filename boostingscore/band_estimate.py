"""Overall IELTS band estimate from best/average scores across skills."""
from __future__ import annotations

from django.contrib.auth.models import User


def _pct_to_band(pct: float) -> float:
    """Map percentage correct to approximate IELTS band (0–9)."""
    if pct >= 95:
        return 9.0
    if pct >= 88:
        return 8.5
    if pct >= 82:
        return 8.0
    if pct >= 75:
        return 7.5
    if pct >= 67:
        return 7.0
    if pct >= 58:
        return 6.5
    if pct >= 50:
        return 6.0
    if pct >= 42:
        return 5.5
    if pct >= 33:
        return 5.0
    if pct >= 25:
        return 4.5
    return 4.0


def _round_ielts_band(value: float) -> float:
    return round(value * 2) / 2


def get_skill_bands(user: User) -> dict:
    """Return per-skill band estimates and whether each skill has data."""
    bands: dict[str, float | None] = {
        "reading": None,
        "writing": None,
        "listening": None,
        "speaking": None,
    }

    try:
        from reading.models import IELTSTestResult, ReadingTestResult

        reading_bands = []
        for row in ReadingTestResult.objects.filter(user=user).exclude(band__isnull=True):
            try:
                reading_bands.append(float(row.band))
            except (TypeError, ValueError):
                pass
        for row in IELTSTestResult.objects.filter(student=user).exclude(band__isnull=True):
            try:
                reading_bands.append(float(row.band))
            except (TypeError, ValueError):
                pass
        if reading_bands:
            bands["reading"] = _round_ielts_band(sum(reading_bands) / len(reading_bands))
    except Exception:
        pass

    try:
        from writing.models import Essay, WritingTask1Attempt, WritingTask2Attempt

        writing_bands = []
        for qs, field in (
            (Essay.objects.filter(student=user), "band_score"),
            (WritingTask1Attempt.objects.filter(user=user), "band_score"),
            (WritingTask2Attempt.objects.filter(user=user), "band_score"),
        ):
            for row in qs.exclude(**{f"{field}__isnull": True}):
                try:
                    writing_bands.append(float(getattr(row, field)))
                except (TypeError, ValueError):
                    pass
        if writing_bands:
            bands["writing"] = _round_ielts_band(sum(writing_bands) / len(writing_bands))
    except Exception:
        pass

    try:
        from listening.models import ListeningPracticeAttempt

        pcts = [
            a.percent
            for a in ListeningPracticeAttempt.objects.filter(student=user)
            if a.total
        ]
        if pcts:
            avg_pct = sum(pcts) / len(pcts)
            bands["listening"] = _pct_to_band(avg_pct)
    except Exception:
        pass

    try:
        from practice_test.models import SpeakingResponse, TestSession

        speaking_bands = []
        for row in SpeakingResponse.objects.filter(user=user).exclude(band__isnull=True):
            try:
                speaking_bands.append(float(row.band))
            except (TypeError, ValueError):
                pass
        for row in TestSession.objects.filter(user=user).exclude(band_speaking__isnull=True):
            try:
                speaking_bands.append(float(row.band_speaking))
            except (TypeError, ValueError):
                pass
        if speaking_bands:
            bands["speaking"] = _round_ielts_band(sum(speaking_bands) / len(speaking_bands))
    except Exception:
        pass

    diag = getattr(getattr(user, "profile", None), "diagnostic_results", None) or {}
    for skill in ("reading", "writing", "listening", "speaking"):
        if bands[skill] is None and diag.get(skill):
            try:
                bands[skill] = float(diag[skill])
            except (TypeError, ValueError):
                pass

    return bands


def get_overall_band_estimate(user: User) -> dict:
    """Combined overall band + per-skill breakdown."""
    bands = get_skill_bands(user)
    available = [b for b in bands.values() if b is not None]
    overall = _round_ielts_band(sum(available) / len(available)) if available else None
    return {
        "overall": overall,
        "skills": bands,
        "skills_with_data": len(available),
        "skills_total": 4,
    }
