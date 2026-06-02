from django.shortcuts import redirect, render


def landing_view(request):
    """Public marketing landing page at `/`.

    Logged-in users are bounced to the authenticated dashboard at `/home/`
    so they don't see the marketing page once they're already signed in.
    """
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "landing.html")
