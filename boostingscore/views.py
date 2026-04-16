from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from .forms import EmailLoginForm, SignUpForm
from .models import UserProfile


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        from .dashboard import flat_home_page_context, home_dashboard_context

        try:
            dash = home_dashboard_context(user, self.request)
            ctx["dashboard"] = dash
        except Exception:
            dash = {}
            ctx["dashboard"] = {}

        try:
            ctx.update(flat_home_page_context(user, self.request))
        except Exception:
            ctx.setdefault("band_score", None)
            ctx.setdefault("words_learned", 0)
            ctx.setdefault("words_pct", 0)
            ctx.setdefault("passages_done", 0)
            ctx.setdefault("streak", 0)
            ctx.setdefault("best_streak", 0)
            ctx.setdefault("essays_count", 0)
            ctx.setdefault("wordbank_count", 0)
            ctx.setdefault("recent_activity", [])

        ctx["greeting"] = dash.get("dash_greeting", "Hello")
        ctx["due_count"] = int(dash.get("dash_vocab_due") or 0)
        ctx["mastered_pct"] = int(dash.get("dash_vocab_pct") or 0)
        ctx["mastered_count"] = int(dash.get("dash_vocab_mastered") or 0)
        ctx["reading_pct"] = int(dash.get("dash_reading_pct") or 0)
        ctx["reading_done"] = int(dash.get("dash_passages") or 0)
        ctx["essays_done"] = int(dash.get("dash_essay_count") or 0)

        words_this_week = 0
        try:
            from vocabulary.models import VocabularyProgress

            week_ago = timezone.now() - timedelta(days=7)
            words_this_week = VocabularyProgress.objects.filter(
                student=user, last_reviewed__gte=week_ago
            ).count()
        except Exception:
            words_this_week = 0
        ctx["words_this_week"] = words_this_week

        return ctx


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("placement:start")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    return render(request, "404.html", status=404)


@login_required
def profile_settings(request: HttpRequest) -> HttpResponse:
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    level_labels = {1: "Beginner", 2: "Standard", 3: "Advanced"}
    return render(
        request,
        "profile_settings.html",
        {
            "profile": profile,
            "level_label": level_labels.get(profile.level, str(profile.level)),
        },
    )


class EmailLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = EmailLoginForm
