from django.urls import path

from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_home, name="home"),
    path("", views.reading_home, name="index"),
    path("home/", views.reading_home, name="reading_home"),
    path("ielts/", views.ielts_practice, name="ielts_practice"),
    path("ielts/", views.ielts_practice, name="ielts"),
    path("ielts/<int:test_id>/", views.ielts_exam, name="ielts_exam"),
    path("ielts/generate/", views.generate_ielts_test, name="generate_ielts_test"),
    path("ielts/submit/", views.submit_ielts_test, name="submit_ielts_test"),
    path("strategies/", views.strategies, name="strategies"),
    path("strategies/skills/", views.skills, name="skills"),
    path("general/", views.general_reading, name="general"),
]
