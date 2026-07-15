"""Public legal / contact pages."""
from django.shortcuts import render


def privacy_view(request):
    return render(request, "legal/privacy.html")


def terms_view(request):
    return render(request, "legal/terms.html")


def contact_view(request):
    return render(request, "legal/contact.html")
