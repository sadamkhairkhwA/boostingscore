from django.urls import path

from . import views

app_name = "vocabulary"

urlpatterns = [
    path("", views.vocabulary_home, name="home"),
    path("studio/", views.flashcard_deck, name="index"),
    path("studio/topic/<str:topic>/", views.flashcard_topic, name="flashcard_topic"),
    path(
        "studio/api/topic-ielts/<str:topic>/",
        views.api_topic_ielts,
        name="api_topic_ielts",
    ),
    path("studio/session/", views.flashcard_session, name="flashcard_deck"),
    path("studio/session/rate/", views.flashcard_rate_api, name="flashcard_rate"),
    path("studio/session/save-pending/", views.flashcard_save_pending_api, name="flashcard_save_pending"),
    path("studio/custom-deck/", views.deck_create, name="deck_create"),
    path("studio/custom-deck/save/", views.deck_create_save, name="deck_create_save"),
    path("studio/custom-deck/<int:deck_id>/", views.custom_deck_hub, name="custom_deck"),
    path("studio/custom-deck/<int:deck_id>/edit/", views.deck_edit, name="deck_edit"),
    path("studio/custom-deck/<int:deck_id>/delete/", views.deck_delete, name="deck_delete"),
    path("api/flashcard-set-generate/", views.flashcard_set_generate, name="flashcard_set_generate"),
    path("api/custom-ai-image/", views.custom_ai_image_preview, name="custom_ai_image_preview"),
    path("api/generate-ielts-vocab/", views.generate_ielts_vocab_api, name="generate_ielts_vocab"),
    path("word-list/", views.word_list, name="word_list"),
    path("quiz/setup/", views.quiz_setup, name="quiz_setup"),
    path("quiz/session/", views.quiz_session, name="quiz_session"),
    path("quiz/api/topic-words/<str:topic>/", views.quiz_topic_words_api, name="quiz_topic_words"),
    path(
        "quiz/api/custom-deck-words/<int:deck_id>/",
        views.quiz_custom_deck_words_api,
        name="quiz_custom_deck_words",
    ),
    path("type-it/", views.type_it_deck, name="type_it_deck"),
    # Specific paths must come before ``type-it/<str:deck_id>/`` so e.g. ``feedback`` is not captured as a deck slug.
    path("type-it/session/", views.type_it_session, name="type_it_session"),
    path("type-it/feedback/", views.type_it_feedback, name="type_it_feedback"),
    path(
        "type-it/<str:topic>/<str:level_slug>/words/",
        views.type_it_words_topic_level,
        name="type_it_words_topic_level",
    ),
    path("type-it/<str:deck_id>/words/", views.type_it_words, name="type_it_words"),
    path("type-it/<str:deck_id>/session/", views.type_it_session_page, name="type_it_session_page"),
    path("type-it/<str:deck_id>/", views.type_it_practice, name="type_it_practice"),
    path("favored/", views.favored, name="favored"),
    path("guide/", views.vocabulary_guide, name="guide"),
    path("api/type-it-check/", views.type_it_check_api, name="type_it_check"),
    path("api/type-it-feedback/", views.type_it_feedback, name="type_it_feedback_legacy"),
    path("api/type-it/custom-deck-create/", views.type_it_custom_deck_create_api, name="type_it_custom_deck_create"),
]
