from django.contrib import admin

from .models import (
    TypeItAttempt,
    CustomCard,
    CustomDeck,
    CustomDeckWord,
    TopicIELTSWordCache,
    TypeItResult,
    UserProfile,
    VocabularyProgress,
    Word,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "streak", "best_streak", "placement_completed")


@admin.register(TopicIELTSWordCache)
class TopicIELTSWordCacheAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "updated_at")
    list_filter = ("status",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "topic", "level", "topic_pack_id")
    list_filter = ("topic", "level")
    search_fields = ("word", "definition")


@admin.register(VocabularyProgress)
class VocabularyProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "word", "mastery_level", "next_review", "is_favored")
    list_filter = ("mastery_level", "is_favored")


@admin.register(TypeItResult)
class TypeItResultAdmin(admin.ModelAdmin):
    list_display = ("student", "band_score", "created_at")


@admin.register(TypeItAttempt)
class TypeItAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "word", "deck_slug", "mode", "total_score", "assisted", "created_at")
    list_filter = ("deck_slug", "assisted")


@admin.register(CustomDeck)
class CustomDeckAdmin(admin.ModelAdmin):
    list_display = ("name", "student", "created_at")


@admin.register(CustomCard)
class CustomCardAdmin(admin.ModelAdmin):
    list_display = ("word", "deck", "student")


@admin.register(CustomDeckWord)
class CustomDeckWordAdmin(admin.ModelAdmin):
    list_display = ("word", "deck", "created_at")
