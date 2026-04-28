from django.contrib import admin

from .models import Essay, LessonProgress, SkillProgress, WritingTask1Attempt, WritingTask2Attempt


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ("student", "task_type", "band_score", "word_count", "created_at")


@admin.register(WritingTask1Attempt)
class WritingTask1AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "question_id",
        "question_type",
        "band_score",
        "word_count",
        "completed_at",
    )
    list_filter = ("question_type",)
    search_fields = ("user__username", "response_text")


@admin.register(WritingTask2Attempt)
class WritingTask2AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "question_id",
        "essay_type",
        "band_score",
        "word_count",
        "completed_at",
    )
    list_filter = ("essay_type",)
    search_fields = ("user__username", "response_text")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson_id", "completed_at")
    search_fields = ("user__username", "lesson_id")


@admin.register(SkillProgress)
class SkillProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "skill_id", "completed_at")
    search_fields = ("user__username", "skill_id")
