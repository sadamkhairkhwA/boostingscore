from django.urls import path

from . import views

app_name = "listening"

urlpatterns = [
    path("", views.listening_home, name="home"),
    path("tips/", views.tips, name="tips"),
    path("practice/<slug:qtype>/", views.practice, name="practice"),
]
