"""Profile page: account edits, placement, stats, plan, delete account."""
from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from boostingscore.email_verification import (
    load_email_change_token,
    send_email_change_verification,
)
from boostingscore.placement_content import can_retake
from vocabulary.models import UserProfile

logger = logging.getLogger(__name__)

FREE_PLAN_BLURB = (
    "Free plan includes Practice Test 1 (all four sections), Reading Test 1, "
    "flashcards, listening multiple-choice practice, and 1 scored attempt each "
    "for writing Task 1 and Task 2, with 10 AI checks per day."
)


def _get_profile(user) -> UserProfile:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def _stats_for_user(user) -> dict:
    words_learned = mastered_pct = tests_taken = 0
    streak = best_streak = 0
    best_band_score = None

    try:
        from vocabulary.models import VocabularyProgress

        all_prog = VocabularyProgress.objects.filter(student=user)
        words_learned = all_prog.count()
        mastered = all_prog.filter(mastery_level=5).count()
        mastered_pct = round(mastered / words_learned * 100) if words_learned else 0
    except Exception:
        pass

    try:
        profile = user.profile
        streak = profile.streak or 0
        best_streak = profile.best_streak or 0
    except Exception:
        pass

    try:
        from reading.models import IELTSTestResult, ReadingAttempt, ReadingTestResult

        tests_taken = (
            ReadingTestResult.objects.filter(user=user).count()
            + IELTSTestResult.objects.filter(student=user).count()
            + ReadingAttempt.objects.filter(student=user, completed=True).count()
        )
    except Exception:
        pass

    try:
        from writing.models import Essay, WritingTask1Attempt, WritingTask2Attempt

        bands = []
        for qs, field in (
            (Essay.objects.filter(student=user), "band_score"),
            (WritingTask1Attempt.objects.filter(user=user), "band_score"),
            (WritingTask2Attempt.objects.filter(user=user), "band_score"),
        ):
            top = qs.exclude(**{f"{field}__isnull": True}).order_by(f"-{field}").first()
            if top is not None and getattr(top, field, None) is not None:
                bands.append(float(getattr(top, field)))
        if bands:
            best_band_score = max(bands)
    except Exception:
        pass

    return {
        "words_learned": words_learned,
        "mastered_pct": mastered_pct,
        "streak": streak,
        "best_streak": best_streak,
        "tests_taken": tests_taken,
        "best_band_score": best_band_score,
    }


def _delete_user_completely(user: User) -> None:
    """Remove user and related data. CASCADE covers most FKs; clear media first."""
    try:
        from practice_test.models import SpeakingResponse

        for resp in SpeakingResponse.objects.filter(user=user):
            if resp.audio:
                try:
                    resp.audio.delete(save=False)
                except Exception:
                    pass
    except Exception as exc:
        logger.warning("speaking audio cleanup: %s", exc)

    user_id = user.pk
    with transaction.atomic():
        user.delete()
    logger.info("deleted user id=%s", user_id)


@login_required
@require_http_methods(["GET", "POST"])
def profile_settings(request):
    profile = _get_profile(request.user)
    user = request.user
    errors: dict[str, str] = {}
    active_form = ""

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        active_form = action

        if action == "display_name":
            name = (request.POST.get("display_name") or "").strip()[:30]
            if not name:
                errors["display_name"] = "Enter a display name."
            else:
                user.first_name = name
                user.save(update_fields=["first_name"])
                messages.success(request, "Display name updated.")
                return redirect("profile_settings")

        elif action == "change_email":
            new_email = (request.POST.get("new_email") or "").strip().lower()
            password = request.POST.get("current_password_email") or ""
            if not user.check_password(password):
                errors["change_email"] = "Current password is incorrect."
            elif not new_email or "@" not in new_email:
                errors["change_email"] = "Enter a valid email address."
            elif new_email == (user.email or "").lower():
                errors["change_email"] = "That is already your current email."
            elif User.objects.filter(email__iexact=new_email).exclude(pk=user.pk).exists():
                errors["change_email"] = "An account with this email already exists."
            else:
                ok, msg = send_email_change_verification(request, user, new_email)
                if ok:
                    messages.success(request, msg)
                else:
                    messages.error(request, msg)
                return redirect("profile_settings")

        elif action == "cancel_pending_email":
            profile.pending_email = ""
            profile.pending_email_sent_at = None
            profile.save(update_fields=["pending_email", "pending_email_sent_at"])
            messages.success(request, "Pending email change cancelled.")
            return redirect("profile_settings")

        elif action == "change_password":
            current = request.POST.get("current_password") or ""
            new1 = request.POST.get("new_password1") or ""
            new2 = request.POST.get("new_password2") or ""
            if not user.check_password(current):
                errors["change_password"] = "Current password is incorrect."
            elif len(new1) < 8:
                errors["change_password"] = "New password must be at least 8 characters."
            elif new1 != new2:
                errors["change_password"] = "New passwords do not match."
            else:
                user.set_password(new1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated.")
                return redirect("profile_settings")

    retake_ok, days_left = can_retake(profile)
    placement = profile.placement_results if profile.placement_completed else None
    stats = _stats_for_user(user)

    return render(
        request,
        "profile/page.html",
        {
            "profile": profile,
            "display_name": user.first_name or "",
            "pending_email": profile.pending_email,
            "placement": placement,
            "placement_taken_at": profile.placement_taken_at,
            "placement_retake_ok": retake_ok,
            "placement_days_left": days_left,
            "show_placement_prompt": not profile.placement_completed,
            "stats": stats,
            "free_plan_blurb": FREE_PLAN_BLURB,
            "is_free_plan": (profile.plan or "free") == "free",
            "plan_label": (profile.plan or "free").title(),
            "errors": errors,
            "active_form": active_form,
            "level_badge_text": profile.level_badge_text,
        },
    )


def verify_email_change(request, token: str):
    """Confirm pending email from the signed link (login optional until applied)."""
    try:
        data = load_email_change_token(token)
        uid = int(data["uid"])
        new_email = (data.get("email") or "").lower().strip()
    except Exception:
        return render(
            request,
            "profile/email_verify_result.html",
            {"ok": False, "message": "This confirmation link is invalid or has expired."},
        )

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return render(
            request,
            "profile/email_verify_result.html",
            {"ok": False, "message": "This confirmation link is no longer valid."},
        )

    profile, _ = UserProfile.objects.get_or_create(user=user)
    if (profile.pending_email or "").lower() != new_email:
        return render(
            request,
            "profile/email_verify_result.html",
            {
                "ok": False,
                "message": "This confirmation link does not match a pending email change.",
            },
        )

    if User.objects.filter(email__iexact=new_email).exclude(pk=user.pk).exists():
        profile.pending_email = ""
        profile.pending_email_sent_at = None
        profile.save(update_fields=["pending_email", "pending_email_sent_at"])
        return render(
            request,
            "profile/email_verify_result.html",
            {"ok": False, "message": "That email is already used by another account."},
        )

    user.email = new_email
    user.save(update_fields=["email"])
    profile.pending_email = ""
    profile.pending_email_sent_at = None
    profile.save(update_fields=["pending_email", "pending_email_sent_at"])

    return render(
        request,
        "profile/email_verify_result.html",
        {
            "ok": True,
            "message": f"Your email is now {new_email}.",
            "logged_in": request.user.is_authenticated and request.user.pk == user.pk,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def profile_delete(request):
    user = request.user
    error = ""
    if request.method == "POST":
        confirm_email = (request.POST.get("confirm_email") or "").strip().lower()
        password = request.POST.get("password") or ""
        expected = (user.email or "").lower()
        if not expected:
            error = "Your account has no email on file. Contact support to delete it."
        elif confirm_email != expected:
            error = "Type your account email exactly to confirm."
        elif not user.check_password(password):
            error = "Password is incorrect."
        else:
            _delete_user_completely(user)
            logout(request)
            return redirect("account_deleted")

    return render(
        request,
        "profile/delete_confirm.html",
        {
            "error": error,
            "account_email": user.email or "",
        },
    )


def account_deleted(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "profile/deleted.html")
