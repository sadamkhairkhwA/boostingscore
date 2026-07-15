from django.urls import path

from . import views

app_name = "speaking"

urlpatterns = [
    path("", views.speaking_home, name="home"),
]
