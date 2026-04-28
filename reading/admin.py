from django.contrib import admin

from .models import (
    GeneralReadingArticle,
    GeneralReadingBookmark,
    GeneralReadingSession,
    GeneralReadingSummary,
    IELTSTestResult,
    ReadingAttempt,
)


@admin.register(IELTSTestResult)
class IELTSTestResultAdmin(admin.ModelAdmin):
    list_display = ("student", "test_id", "score", "band", "created_at")


@admin.register(ReadingAttempt)
class ReadingAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "test_type", "score", "completed", "created_at")


@admin.register(GeneralReadingArticle)
class GeneralReadingArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "level", "is_featured", "is_active", "updated_at")
    list_filter = ("topic", "level", "is_featured", "is_active")
    search_fields = ("title", "slug")


@admin.register(GeneralReadingSession)
class GeneralReadingSessionAdmin(admin.ModelAdmin):
    list_display = ("student", "article", "score", "total_questions", "wpm", "created_at")
    list_filter = ("article__topic", "article__level")
    search_fields = ("student__username", "article__title")


@admin.register(GeneralReadingBookmark)
class GeneralReadingBookmarkAdmin(admin.ModelAdmin):
    list_display = ("student", "article", "created_at")
    search_fields = ("student__username", "article__title")


@admin.register(GeneralReadingSummary)
class GeneralReadingSummaryAdmin(admin.ModelAdmin):
    list_display = ("student", "article", "updated_at")
    search_fields = ("student__username", "article__title", "summary_text")
