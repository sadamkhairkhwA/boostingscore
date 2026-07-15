"""Placement test views — free, fully auto-graded, no time limit."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from boostingscore.placement_content import PLACEMENT_SECTIONS, can_retake, score_placement
from vocabulary.models import UserProfile

SESSION_STARTED_KEY = "placement_started_at"


def _get_profile(user) -> UserProfile:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def _save_placement(profile: UserProfile, results: dict) -> None:
    profile.placement_completed = True
    profile.placement_score = int(round(results.get("weighted_pct") or 0))
    profile.placement_results = results
    profile.placement_taken_at = timezone.now()
    profile.level = int(results.get("study_level") or profile.level or 1)
    # Keep legacy diagnostic gate satisfied so old redirects don't loop.
    profile.diagnostic_completed = True
    profile.save(
        update_fields=[
            "placement_completed",
            "placement_score",
            "placement_results",
            "placement_taken_at",
            "level",
            "diagnostic_completed",
        ]
    )


def _elapsed_seconds(request):
    """Prefer client-reported duration; fall back to server session start."""
    raw = (request.POST.get("elapsed_seconds") or "").strip()
    client = None
    if raw.isdigit():
        client = int(raw)
        # Sanity: 0–2h (silent analytics only; no UI)
        if client < 0 or client > 7200:
            client = None

    started = request.session.get(SESSION_STARTED_KEY)
    server = None
    if started:
        try:
            server = max(0, int(timezone.now().timestamp() - float(started)))
        except (TypeError, ValueError):
            server = None

    if client is not None and server is not None:
        if server == 0 or abs(client - server) / max(server, 1) <= 0.2:
            return client
        return server
    return client if client is not None else server


@login_required
def placement_intro(request):
    """Post-signup welcome: start or skip the placement test."""
    profile = _get_profile(request.user)
    allowed, days_left = can_retake(profile)

    if profile.placement_completed and not request.session.get("placement_retake"):
        if not allowed:
            return redirect("placement_results")
        return render(
            request,
            "placement/intro.html",
            {
                "is_retake": True,
                "days_left": 0,
                "display_name": (
                    request.user.first_name
                    or (request.user.username.split("@")[0] if request.user.username else "there")
                ),
            },
        )

    if profile.placement_completed and request.session.get("placement_retake") and not allowed:
        request.session.pop("placement_retake", None)
        return redirect("placement_results")

    return render(
        request,
        "placement/intro.html",
        {
            "is_retake": bool(request.session.get("placement_retake")),
            "days_left": days_left,
            "display_name": (
                request.user.first_name
                or (request.user.username.split("@")[0] if request.user.username else "there")
            ),
        },
    )


@login_required
@require_POST
def placement_skip(request):
    """Skip for now → dashboard; card remains until the test is taken."""
    request.session["placement_card_dismissed"] = False
    request.session["show_placement_nudge"] = True
    return redirect("home")


@login_required
@require_POST
def placement_dismiss_card(request):
    """Hide the dashboard nudge for this browser session."""
    request.session["placement_card_dismissed"] = True
    return redirect("home")


@login_required
@require_POST
def placement_retake(request):
    """Start a retake if the 14-day cooldown has passed."""
    profile = _get_profile(request.user)
    allowed, _ = can_retake(profile)
    if not allowed:
        return redirect("home")
    request.session["placement_retake"] = True
    return redirect("placement_test")


@login_required
@require_http_methods(["GET", "POST"])
def placement_test(request):
    profile = _get_profile(request.user)
    retake = bool(request.session.get("placement_retake"))
    allowed, days_left = can_retake(profile)

    if profile.placement_completed and not retake:
        return redirect("placement_results")
    if retake and not allowed:
        request.session.pop("placement_retake", None)
        return redirect("placement_results")

    if request.method == "POST":
        answers = {}
        for key, val in request.POST.items():
            if key.startswith("q_"):
                answers[key[2:]] = val
        results = score_placement(answers)
        results["taken_at"] = timezone.now().isoformat()
        elapsed = _elapsed_seconds(request)
        if elapsed is not None:
            results["elapsed_seconds"] = elapsed
        request.session.pop(SESSION_STARTED_KEY, None)
        _save_placement(profile, results)
        request.session.pop("placement_retake", None)
        request.session.pop("show_placement_nudge", None)
        request.session["placement_just_finished"] = True
        return redirect("placement_results")

    request.session[SESSION_STARTED_KEY] = timezone.now().timestamp()

    return render(
        request,
        "placement/test.html",
        {
            "sections": PLACEMENT_SECTIONS,
            "is_retake": retake,
            "days_left": days_left,
        },
    )


@login_required
def placement_results(request):
    profile = _get_profile(request.user)
    if not profile.placement_completed:
        return redirect("placement")
    results = profile.placement_results or {}
    just_finished = request.session.pop("placement_just_finished", False)
    allowed, days_left = can_retake(profile)
    return render(
        request,
        "placement/results.html",
        {
            "results": results,
            "just_finished": just_finished,
            "can_retake": allowed,
            "days_left": days_left,
            "taken_at": profile.placement_taken_at,
        },
    )
