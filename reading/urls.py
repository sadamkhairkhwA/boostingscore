from django.urls import path

from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_home, name="home"),
    path("question-types/", views.question_types_index, name="question_types_index"),
    path(
        "question-types/<slug:question_type_slug>/learn/",
        views.question_type_learn,
        name="question_type_learn",
    ),
    path(
        "question-types/<slug:question_type_slug>/practice/<int:set_number>/",
        views.question_type_practice,
        name="question_type_practice",
    ),
    path("tests/", views.academic_tests_index, name="academic_tests_index"),
    path("tests/<int:test_number>/", views.academic_test_session, name="academic_test_session"),
    path(
        "tests/<int:test_number>/submit/",
        views.academic_test_submit,
        name="academic_test_submit",
    ),
    path("ielts/", views.ielts_home, name="ielts"),
    path("ielts/1/", views.ielts_exam, name="ielts_exam"),
    path("ielts/generate/", views.generate_ielts_test, name="generate_ielts_test"),
    path("ielts/submit/", views.submit_ielts_test, name="submit_ielts_test"),
    path("strategies/", views.strategies, name="strategies"),
    path("strategies/skills/", views.skills, name="skills"),
    path("general/", views.general_reading, name="general"),
    path(
        "general/summary-feedback/",
        views.general_summary_feedback,
        name="general_summary_feedback",
    ),
    path("general/log-session/", views.general_log_session, name="general_log_session"),
    path(
        "general/toggle-bookmark/",
        views.general_toggle_bookmark,
        name="general_toggle_bookmark",
    ),
    path("vocab-context/", views.vocab_context, name="vocab_context"),
    path("timed-drill/", views.timed_drill_index, name="timed_drill_index"),
    path("timed-drill/<int:part>/", views.timed_drill_session, name="timed_drill_session"),
    path(
        "timed-drill/<int:part>/submit/",
        views.timed_drill_submit,
        name="timed_drill_submit",
    ),
]
