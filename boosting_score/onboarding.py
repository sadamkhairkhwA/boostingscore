from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def welcome_view(request):
    """First-time onboarding page for newly-signed-up users.

    GET  → renders the welcome screen (logo, hero, level picker, first steps).
    POST → saves the chosen starting level and sends the user to the dashboard.

    Existing users who land here still see a useful setup page; submitting the
    form just confirms their current level.
    """
    from vocabulary.models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        try:
            level = int(request.POST.get("level", profile.level or 1))
        except (TypeError, ValueError):
            level = profile.level or 1
        if level not in (1, 2, 3):
            level = 1
        profile.level = level
        if hasattr(profile, "placement_completed"):
            profile.placement_completed = True
        profile.save()
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
