from django.urls import path

from . import views

app_name = "practice_test"

urlpatterns = [
    path("", views.tests, name="tests"),
    path("hub/", views.hub, name="hub"),

    # Exam intro / "Start exam" instructions screen (one per section)
    path("start/<slug:section>/", views.exam_intro, name="exam_intro"),

    # --- Standalone single-section practice (no shared state with the full test) ---
    path("listening/",          views.listening,         name="listening"),
    path("listening/prepare/",  views.listening_prepare, name="listening_prepare"),
    path("listening/submit/",   views.listening_submit,  name="listening_submit"),
    path("reading/",            views.reading,           name="reading"),
    path("reading/submit/",     views.reading_submit,    name="reading_submit"),
    path("writing/",            views.writing,           name="writing"),
    path("writing/submit/",     views.writing_submit,    name="writing_submit"),
    path("speaking/",                            views.speaking,              name="speaking"),
    path("speaking/submit-answer/",              views.speaking_submit_answer, name="speaking_submit_answer"),
    path("speaking/finish/",                     views.speaking_finish,        name="speaking_finish"),
    path("speaking/results/<int:session_id>/",   views.speaking_results,       name="speaking_results"),

    # Async API endpoints (shared)
    path("api/speaking/score/",   views.speaking_score_api, name="speaking_score_api"),
    path("api/speaking/rescore/<int:response_id>/", views.speaking_rescore_api, name="speaking_rescore_api"),

    # --- Full Academic Test (dedicated, separate from standalone) ---
    path("full/",                views.full_test,            name="full"),
    path("full/reading/",        views.full_reading,         name="full_reading"),
    path("full/reading/submit/", views.full_reading_submit,  name="full_reading_submit"),
    path("full/writing/",        views.full_writing,         name="full_writing"),
    path("full/writing/submit/", views.full_writing_submit,  name="full_writing_submit"),
    path("full/listening/",         views.full_listening,        name="full_listening"),
    path("full/listening/submit/",  views.full_listening_submit, name="full_listening_submit"),
    path("full/speaking/",       views.full_speaking,        name="full_speaking"),
    path("full/finish/",         views.full_finish,          name="full_finish"),

    # Results
    path("results/<int:session_id>/", views.results, name="results"),
]
