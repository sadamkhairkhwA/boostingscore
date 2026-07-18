from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from .models import (
    AiUsageLog,
    CustomCard,
    CustomDeck,
    CustomDeckWord,
    DailyAiUsage,
    FeedbackSubmission,
    SiteSettings,
    TopicIELTSWordCache,
    TypeItAttempt,
    TypeItResult,
    UserProfile,
    VocabularyProgress,
    Word,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Single-object page: the sidebar link opens the edit form directly."""

    fields = ("maintenance_mode", "maintenance_message")

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = SiteSettings.load()
        return redirect(
            reverse("admin:vocabulary_sitesettings_change", args=[obj.pk])
        )

    def save_model(self, request, obj, form, change):
        obj.pk = 1
        super().save_model(request, obj, form, change)
        # Re-read from DB so the message reflects what visitors will hit.
        fresh = SiteSettings.objects.filter(pk=1).values("maintenance_mode").first()
        on = bool(fresh and fresh["maintenance_mode"])
        self.message_user(
            request,
            (
                "Maintenance mode is ON — anonymous visitors now get HTTP 503."
                if on
                else "Maintenance mode is OFF — the site is public again."
            ),
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Show signed-up accounts with email, verification status, plan, and join date.
admin.site.unregister(User)


class PlanFilter(admin.SimpleListFilter):
    """Filter users by their profile plan (free/premium/...)."""

    title = "plan"
    parameter_name = "plan"

    def lookups(self, request, model_admin):
        plans = (
            UserProfile.objects.order_by()
            .values_list("plan", flat=True)
            .distinct()
        )
        return [(p or "free", (p or "free").title()) for p in plans]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(profile__plan=self.value())
        return queryset


class VerifiedFilter(admin.SimpleListFilter):
    """Email verification = account activated via the signup link."""

    title = "email verified"
    parameter_name = "verified"

    def lookups(self, request, model_admin):
        return [("yes", "Verified"), ("no", "Not verified")]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(is_active=True)
        if self.value() == "no":
            return queryset.filter(is_active=False)
        return queryset


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "date_joined",
        "is_active",
        "verified",
        "plan",
        "is_staff",
        "last_login",
    )
    list_filter = (VerifiedFilter, PlanFilter, "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")

    @admin.display(description="Email verified", boolean=True, ordering="is_active")
    def verified(self, obj):
        # Signup creates accounts inactive; the email link activates them.
        return obj.is_active

    @admin.display(description="Plan")
    def plan(self, obj):
        try:
            return (obj.profile.plan or "free").title()
        except UserProfile.DoesNotExist:
            return "Free"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "user_email",
        "plan",
        "level",
        "streak",
        "best_streak",
        "placement_completed",
    )
    search_fields = ("user__username", "user__email", "user__first_name")
    list_filter = ("plan", "level", "placement_completed")

    @admin.display(description="Email", ordering="user__email")
    def user_email(self, obj):
        return obj.user.email or "—"


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


@admin.register(DailyAiUsage)
class DailyAiUsageAdmin(admin.ModelAdmin):
    list_display = ("user", "usage_date", "count")
    list_filter = ("usage_date",)
    search_fields = ("user__username",)


@admin.register(AiUsageLog)
class AiUsageLogAdmin(admin.ModelAdmin):
    list_display = ("user", "feature", "created_at")
    list_filter = ("feature", "created_at")
    search_fields = ("user__username", "feature")
    readonly_fields = ("user", "feature", "created_at")


@admin.register(FeedbackSubmission)
class FeedbackSubmissionAdmin(admin.ModelAdmin):
    list_display = ("feedback_type", "short_message", "page_url", "user", "created_at")
    list_filter = ("feedback_type",)
    search_fields = ("email", "message", "page_url", "user__username", "user__email")
    readonly_fields = (
        "user",
        "email",
        "feedback_type",
        "message",
        "page_url",
        "user_agent",
        "created_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_display_links = ("short_message",)

    @admin.display(description="Message", ordering="message")
    def short_message(self, obj):
        text = (obj.message or "").strip()
        return text if len(text) <= 80 else text[:77] + "…"
