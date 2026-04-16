from django.urls import path

from . import views

app_name = "vocabulary"

urlpatterns = [
    path("", views.vocabulary_home, name="home"),
    path("home/", views.vocabulary_home, name="vocabulary_home"),
    path("favored/", views.favored_redirect, name="favored"),
    path("guide/", views.vocabulary_guide, name="guide"),
    path("studio/", views.flashcards, name="index"),
    path("pick/", views.flashcards, name="flashcard"),
    path("word-list/", views.word_list_page, name="word_list"),
    path("quiz/setup/", views.quiz_setup_page, name="quiz_setup"),
    path("quiz/setup/words/", views.quiz_setup_words, name="quiz_setup_words"),
    path("type-it/decks/", views.type_it_deck_select, name="type_it_deck_select"),
    path("type-it/session/", views.type_it_session, name="type_it_session"),
    path("type-it/check/", views.type_it_check_api, name="type_it_check_api"),
    path("type-it/result/", views.type_it_session_result, name="type_it_session_result"),
    path("struggling/", views.struggling_practice, name="struggling"),
    path(
        "progress/flashcard-rating/",
        views.progress_flashcard_rating,
        name="progress_flashcard_rating",
    ),
    path(
        "progress/session-end/",
        views.progress_session_end,
        name="progress_session_end",
    ),
    path(
        "progress/review-settings/",
        views.progress_review_settings,
        name="progress_review_settings",
    ),
    path("decks/create/", views.deck_create, name="deck_create"),
    path("decks/create/save/", views.deck_create_save, name="deck_create_save"),
    path("set/ai/", views.flashcard_set_create, name="flashcard_set_create"),
    path("set/ai/generate/", views.flashcard_set_generate, name="flashcard_set_generate"),
    path("set/ai/save/", views.flashcard_set_save, name="flashcard_set_save"),
    path("custom/new/", views.custom_create, name="custom_create"),
    path("custom/<int:pk>/edit/", views.custom_edit, name="custom_edit"),
    path("custom/<int:pk>/delete/", views.custom_delete, name="custom_delete"),
    path("custom/<int:pk>/master/", views.custom_master, name="custom_master"),
    path("custom/<int:pk>/reviewed/", views.custom_reviewed, name="custom_reviewed"),
    path("custom/ai-fill/", views.custom_ai_fill, name="custom_ai_fill"),
    path("custom/ai-image/", views.custom_ai_image_preview, name="custom_ai_image_preview"),
    path(
        "custom/<int:pk>/ai-image/",
        views.custom_ai_image_save,
        name="custom_ai_image_save",
    ),
    path("type/check-sentence/", views.type_check_sentence, name="type_check_sentence"),
    path("favorites/toggle/", views.vocab_toggle_favorite, name="vocab_toggle_favorite"),
    path(
        "word-list/word-bank/",
        views.word_bank_add_from_vocab,
        name="word_bank_add_vocab",
    ),
]
