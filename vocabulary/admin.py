from django.contrib import admin

from .models import CustomCard, CustomDeck, VocabFavorite, VocabularyProgress, Word


@admin.register(CustomDeck)
class CustomDeckAdmin(admin.ModelAdmin):
    list_display = ("name", "student", "created_at", "card_count")
    list_filter = ("created_at",)
    search_fields = ("name", "student__username")
    raw_id_fields = ("student",)
    ordering = ("-created_at",)

    @admin.display(description="Cards")
    def card_count(self, obj: CustomDeck) -> int:
        return obj.cards.count()


@admin.register(CustomCard)
class CustomCardAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "student",
        "deck",
        "topic",
        "level",
        "part_of_speech",
        "is_mastered",
        "has_definition_image",
        "review_count",
        "next_review_at",
        "created_at",
    )
    list_filter = ("topic", "level", "is_mastered")
    search_fields = ("word", "definition", "student__username")
    raw_id_fields = ("student", "deck")
    ordering = ("-created_at",)

    @admin.display(description="Image", boolean=True)
    def has_definition_image(self, obj: CustomCard) -> bool:
        return bool(obj.definition_image)


@admin.register(VocabularyProgress)
class VocabularyProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "word",
        "custom_card",
        "mastery_level",
        "times_seen",
        "times_correct",
        "times_marked_hard",
        "sessions_seen",
        "last_session_date",
    )
    list_filter = ("mastery_level", "last_session_date")
    raw_id_fields = ("student", "word", "custom_card")
    search_fields = ("word__word", "custom_card__word", "student__username")
    ordering = ("-last_reviewed",)


@admin.register(VocabFavorite)
class VocabFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "custom_card", "created_at")
    list_filter = ("created_at",)
    raw_id_fields = ("user", "word", "custom_card")
    ordering = ("-created_at",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "topic",
        "level",
        "part_of_speech",
        "has_definition_image",
        "definition_preview",
    )
    list_filter = ("topic", "level")
    search_fields = ("word", "definition", "example_sentence", "part_of_speech")
    ordering = ("topic", "level", "word")

    @admin.display(description="Image", boolean=True)
    def has_definition_image(self, obj: Word) -> bool:
        return bool(obj.definition_image)

    @admin.display(description="Definition")
    def definition_preview(self, obj: Word) -> str:
        text = (obj.definition or "").strip()
        if len(text) > 60:
            return text[:57] + "…"
        return text or "—"
