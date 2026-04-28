from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views as home_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", home_views.signup_view, name="signup"),
    path("accounts/profile/", home_views.profile_settings, name="profile_settings"),
    path("", home_views.home_view, name="home"),
    path("vocabulary/", include("vocabulary.urls", namespace="vocabulary")),
    path("reading/", include("reading.urls", namespace="reading")),
    path("writing/", include("writing.urls", namespace="writing")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
