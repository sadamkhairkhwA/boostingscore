from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def welcome_view(request):
    """Legacy level picker — new users go through the placement test instead."""
    from vocabulary.models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not profile.placement_completed:
        return redirect("placement")

    if request.method == "POST":
        try:
            level = int(request.POST.get("level", profile.level or 1))
        except (TypeError, ValueError):
            level = profile.level or 1
        if level not in (1, 2, 3):
            level = 1
        profile.level = level
        profile.placement_completed = True
        profile.save(update_fields=["level", "placement_completed"])
        return redirect("home")

    return render(
        request,
        "welcome.html",
        {
            "current_level": profile.level or 1,
            "display_name": (
                request.user.first_name
                or (request.user.username.split("@")[0] if request.user.username else "there")
            ),
        },
    )
