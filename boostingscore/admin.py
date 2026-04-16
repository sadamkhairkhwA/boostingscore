from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "level",
        "placement_completed",
        "review_easy_days",
        "review_hard_days",
        "review_session_size",
    )
    list_filter = ("level", "placement_completed")
    search_fields = ("user__username", "user__email")
