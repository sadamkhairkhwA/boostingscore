from django.contrib import admin

from .models import ListeningPracticeAttempt


@admin.register(ListeningPracticeAttempt)
class ListeningPracticeAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "question_type", "set_id", "score", "total", "created_at")
    list_filter = ("question_type", "created_at")
    search_fields = ("student__username", "set_id")
