from django.shortcuts import redirect
from django.urls import reverse

from .models import UserProfile


class PlacementRequiredMiddleware:
    """
    Send authenticated users with placement_completed=False to the placement test.
    """

    PREFIXES = (
        "/placement-test/",
        "/admin/",
        "/accounts/login",
        "/accounts/logout",
        "/accounts/signup",
        "/accounts/profile",
        "/static/",
        "/media/",
        "/favicon.ico",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and request.method == "GET":
            path = request.path
            if not any(path.startswith(p) for p in self.PREFIXES):
                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={"level": 2, "placement_completed": False},
                )
                if not profile.placement_completed:
                    return redirect(reverse("placement:start"))
        return self.get_response(request)
