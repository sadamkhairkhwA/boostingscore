from django import forms
from django.contrib import admin
from django.db import models as dj_models
from django.db.models import QuerySet

from .models import IELTSTest, IELTSTestContent, IELTSTestResult


class IELTSTestContentInline(admin.StackedInline):
    model = IELTSTestContent
    extra = 1
    fields = ["content_json", "version", "is_current"]
    formfield_overrides = {
        dj_models.JSONField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 40,
                    "cols": 120,
                    "style": "font-family: monospace; font-size: 12px;",
                }
            )
        }
    }


@admin.register(IELTSTest)
class IELTSTestAdmin(admin.ModelAdmin):
    list_display = (
        "test_number",
        "topic",
        "band_range",
        "difficulty",
        "total_questions",
        "time_limit",
        "is_active",
        "is_published",
        "has_content",
        "created_at",
    )
    list_filter = ("difficulty", "is_active", "is_published")
    list_editable = ("is_active", "is_published")
    search_fields = ("topic", "band_range")
    ordering = ("test_number",)
    inlines = [IELTSTestContentInline]
    actions = ("publish_tests", "unpublish_tests", "mark_active", "mark_inactive")

    @admin.display(boolean=True, description="Has content")
    def has_content(self, test: IELTSTest) -> bool:
        return test.contents.filter(is_current=True).exists()

    @admin.action(description="Publish selected tests")
    def publish_tests(self, request, queryset: QuerySet[IELTSTest]):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} tests published successfully.")

    @admin.action(description="Unpublish selected tests")
    def unpublish_tests(self, request, queryset: QuerySet[IELTSTest]):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} tests unpublished.")

    @admin.action(description="Mark selected tests active")
    def mark_active(self, request, queryset: QuerySet[IELTSTest]):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} tests marked active.")

    @admin.action(description="Mark selected tests inactive")
    def mark_inactive(self, request, queryset: QuerySet[IELTSTest]):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} tests marked inactive.")


@admin.register(IELTSTestContent)
class IELTSTestContentAdmin(admin.ModelAdmin):
    list_display = ("test", "version", "is_current", "generated_at")
    list_filter = ("is_current",)
    list_editable = ("is_current",)
    formfield_overrides = {
        dj_models.JSONField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 50,
                    "cols": 120,
                    "style": "font-family: monospace; font-size: 12px;",
                }
            )
        }
    }


@admin.register(IELTSTestResult)
class IELTSTestResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "test",
        "score",
        "total_questions",
        "percentage",
        "band_estimate",
        "time_seconds",
        "completed_at",
    )
    list_filter = ("test", "completed_at")
    search_fields = ("student__username",)
    readonly_fields = (
        "student",
        "test",
        "score",
        "total_questions",
        "time_seconds",
        "answers_json",
        "completed_at",
    )
