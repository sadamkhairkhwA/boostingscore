from django.contrib import admin

from .models import SpeakingResponse, TestSession


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "kind", "status", "band_overall", "started_at")
    list_filter = ("kind", "status")
    search_fields = ("user__username",)


@admin.register(SpeakingResponse)
class SpeakingResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "part", "question_index", "band", "created_at")
    list_filter = ("part",)
    search_fields = ("user__username", "question_text", "transcript")
