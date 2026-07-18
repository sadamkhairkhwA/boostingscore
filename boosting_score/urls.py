from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve as media_serve

import views as home_views
from boosting_score.landing import landing_view
from boosting_score.onboarding import welcome_view
from boostingscore.diagnostic_views import diagnostic_view, diagnostic_results_view
from boostingscore.feedback_views import feedback_submit
from boostingscore.legal_views import privacy_view, terms_view, contact_view
from boostingscore.placement_views import (
    placement_dismiss_card,
    placement_intro,
    placement_results,
    placement_retake,
    placement_skip,
    placement_test,
)

from boostingscore.profile_views import (
    account_deleted,
    profile_delete,
    profile_settings,
    verify_email_change,
)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", home_views.login_view, name="login"),
    # Branded HTML password-reset email; overrides the include() default below.
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            html_email_template_name="registration/password_reset_email_html.html",
        ),
        name="password_reset",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", home_views.signup_view, name="signup"),
    path("accounts/signup/check-email/", home_views.signup_check_email, name="signup_check_email"),
    path("accounts/signup/resend/", home_views.signup_resend_verification, name="signup_resend_verification"),
    path("accounts/signup/verify-code/", home_views.signup_verify_code, name="signup_verify_code"),
    path("accounts/profile/", profile_settings, name="profile_settings"),
    path("accounts/profile/delete/", profile_delete, name="profile_delete"),
    path("accounts/deleted/", account_deleted, name="account_deleted"),
    path(
        "accounts/verify-email/<path:token>/",
        verify_email_change,
        name="profile_verify_email",
    ),
    path("accounts/speaking-ai-notice/", home_views.speaking_ai_notice_ack, name="speaking_ai_notice_ack"),
    path("feedback/", feedback_submit, name="feedback_submit"),
    path("", landing_view, name="landing"),
    path("welcome/", welcome_view, name="welcome"),
    path("privacy/", privacy_view, name="privacy"),
    path("terms/", terms_view, name="terms"),
    path("contact/", contact_view, name="contact"),
    path("placement/", placement_intro, name="placement"),
    path("placement/test/", placement_test, name="placement_test"),
    path("placement/results/", placement_results, name="placement_results"),
    path("placement/skip/", placement_skip, name="placement_skip"),
    path("placement/dismiss/", placement_dismiss_card, name="placement_dismiss"),
    path("placement/retake/", placement_retake, name="placement_retake"),
    path("diagnostic/", diagnostic_view, name="diagnostic"),
    path("diagnostic/results/", diagnostic_results_view, name="diagnostic_results"),
    path("home/", home_views.home_view, name="home"),
    path("vocabulary/", include("vocabulary.urls", namespace="vocabulary")),
    path("reading/", include("reading.urls", namespace="reading")),
    path("writing/", include("writing.urls", namespace="writing")),
    path("test/", include("practice_test.urls", namespace="practice_test")),
    path("listening/", include("listening.urls", namespace="listening")),
    path("speaking/", include("speaking.urls", namespace="speaking")),
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
