from django.urls import path

from . import views

app_name = "writing"

urlpatterns = [
    path("", views.writing_home, name="home"),
    path("task1/", views.task1_browser, name="task1"),
    path("task1/<int:question_id>/feedback/", views.task1_feedback_page_by_id, name="task1_feedback_page_by_id"),
    path("task1/<slug:question_type>/", views.task1_question_list, name="task1_question_list"),
    path(
        "task1/<slug:question_type>/<int:question_id>/",
        views.task1_question_page,
        name="task1_question_page",
    ),
    path(
        "task1/<slug:question_type>/<int:question_id>/feedback/",
        views.task1_feedback_page,
        name="task1_feedback_page",
    ),
    path("task2/", views.task2_browser, name="task2"),
    path("task2/<slug:essay_type>/", views.task2_question_list, name="task2_question_list"),
    path("task2/<slug:essay_type>/<int:q_id>/", views.task2_question_page, name="task2_question_page"),
    path("task2/<slug:essay_type>/<int:q_id>/feedback/", views.task2_feedback_page, name="task2_feedback_page"),
    path("lessons/", views.lessons_hub, name="lessons_hub"),
    path("lessons/grammar/", views.grammar_mistakes, name="grammar_mistakes"),
    path("lessons/<slug:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<slug:lesson_id>/check/", views.lesson_practice_check, name="lesson_practice_check"),
    path("grammar/", views.grammar_hub, name="grammar_hub"),
    path("grammar/<slug:topic_id>/", views.grammar_topic, name="grammar_topic"),
    path("skills/", views.skills_hub, name="skills_hub"),
    path("skills/<slug:skill_id>/", views.skill_detail, name="skill_detail"),
    path("paraphrase/", views.paraphrase, name="paraphrase"),
    path("paraphrase/sentence/", views.paraphrase_sentence_api, name="paraphrase_sentence_api"),
    path("paraphrase/check/", views.paraphrase_check, name="paraphrase_check"),
]
