from django.urls import path

from . import views

app_name = "writing"

urlpatterns = [
    path("", views.writing_home, name="home"),
    path("home/", views.writing_home, name="writing_home"),
    path("task1/", views.writing_task1_redirect, name="task1"),
    path("task2/", views.writing_task2_redirect, name="task2"),
    path("pick/", views.task_chooser, name="pick"),
    path("paraphrase/", views.paraphrase_practice, name="paraphrase"),
    path("question/", views.writing_question, name="question"),
    path("result/<int:pk>/", views.writing_result, name="result"),
    path("word-bank/", views.word_bank, name="word_bank"),
]
