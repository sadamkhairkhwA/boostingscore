from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from .placement_views import placement_retake_prepare
from .views import EmailLoginView, HomeView, profile_settings, signup

handler404 = "boostingscore.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path(
        "accounts/login/",
        EmailLoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("accounts/signup/", signup, name="signup"),
    path(
        "accounts/profile/retake-placement/",
        placement_retake_prepare,
        name="placement_retake",
    ),
    path("accounts/profile/", profile_settings, name="profile_settings"),
    path(
        "placement/",
        RedirectView.as_view(pattern_name="placement:start", permanent=False),
    ),
    path("placement-test/", include("boostingscore.placement_urls")),
    path("vocabulary/", include("vocabulary.urls")),
    path("reading/", include(("reading.urls", "reading"), namespace="reading")),
    path("writing/", include("writing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
