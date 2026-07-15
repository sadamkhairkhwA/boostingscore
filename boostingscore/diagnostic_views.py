"""Post-signup diagnostic test views (legacy — redirects to placement)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def diagnostic_view(request):
    return redirect("placement")


@login_required
def diagnostic_results_view(request):
    from vocabulary.models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.placement_completed:
        return redirect("placement_results")
    return redirect("placement")
