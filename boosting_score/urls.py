from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve as media_serve

import views as home_views
from boosting_score.landing import landing_view
from boosting_score.onboarding import welcome_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", home_views.signup_view, name="signup"),
    path("accounts/profile/", home_views.profile_settings, name="profile_settings"),
    path("", landing_view, name="landing"),
    path("welcome/", welcome_view, name="welcome"),
    path("home/", home_views.home_view, name="home"),
    path("vocabulary/", include("vocabulary.urls", namespace="vocabulary")),
    path("reading/", include("reading.urls", namespace="reading")),
    path("writing/", include("writing.urls", namespace="writing")),
    path("test/", include("practice_test.urls", namespace="practice_test")),
    path("listening/", include("listening.urls", namespace="listening")),
    # Serve user-generated media (e.g. the generated listening MP3) in BOTH
    # dev and production. Django's static() helper only serves media when
    # DEBUG=True, which left /media/ 404ing on Railway — so we wire the serve
    # view explicitly here instead.
    re_path(
        r"^media/(?P<path>.*)$",
        media_serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
