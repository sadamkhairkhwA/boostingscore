from django.contrib import admin

from .models import Essay, ParaphrasePractice, WordBankEntry, WritingCoachingSession, WritingQuestion


@admin.register(WritingQuestion)
class WritingQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "level", "question_type", "prompt_kind", "preview")
    list_filter = ("topic", "level", "question_type", "prompt_kind")
    search_fields = ("question_text",)
    ordering = ("topic", "level", "id")

    @admin.display(description="Question")
    def preview(self, obj: WritingQuestion) -> str:
        t = (obj.question_text or "").strip()
        return (t[:70] + "…") if len(t) > 70 else t or "—"


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "word_count",
        "band_score",
        "submitted_at",
    )
    list_filter = ("question_type", "submitted_at")
    search_fields = ("student_answer", "question", "student__username")
    raw_id_fields = ("student", "writing_question")
    ordering = ("-submitted_at",)


@admin.register(WritingCoachingSession)
class WritingCoachingSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "writing_question", "stage", "updated_at")
    list_filter = ("stage",)
    raw_id_fields = ("student", "writing_question")
    ordering = ("-updated_at",)


@admin.register(ParaphrasePractice)
class ParaphrasePracticeAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "topic", "level", "created_at")
    list_filter = ("level",)
    raw_id_fields = ("student",)
    ordering = ("-created_at",)


@admin.register(WordBankEntry)
class WordBankEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "phrase", "essay", "created_at")
    list_filter = ("created_at",)
    search_fields = ("phrase", "user__username")
    raw_id_fields = ("user", "essay")
