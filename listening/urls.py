from django.urls import path

from . import views

app_name = "listening"

urlpatterns = [
    path("", views.listening_home, name="home"),
    path("tips/", views.tips, name="tips"),
    path("section4-notes/", views.section4_notes_index, name="section4_notes"),
    path(
        "section4-notes/<slug:lecture_id>/",
        views.section4_notes_session,
        name="section4_notes_session",
    ),
    path("detail-drills/", views.detail_drills, name="detail_drills"),
    path("practice/<slug:qtype>/", views.practice, name="practice"),
    path("<slug:qtype>/tests/", views.type_tests, name="type_tests"),
    path("<slug:qtype>/", views.type_detail, name="type_detail"),
]
