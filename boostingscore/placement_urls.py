from django.urls import path

from . import placement_views

app_name = "placement"

urlpatterns = [
    path("", placement_views.placement_start, name="start"),
    path("<int:n>/", placement_views.placement_question, name="question"),
    path("results/", placement_views.placement_results, name="results"),
]
