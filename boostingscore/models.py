from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Per-user vocabulary level (from placement) and completion gate."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    level = models.PositiveSmallIntegerField(
        default=2,
        choices=((1, "Beginner"), (2, "Standard"), (3, "Advanced")),
        help_text="Vocabulary deck level (1–3) from placement test.",
    )
    placement_completed = models.BooleanField(
        default=False,
        help_text="When False, user must complete placement before study areas.",
    )
    review_easy_days = models.PositiveSmallIntegerField(
        default=7,
        help_text="Days until next review after marking a flashcard Easy.",
    )
    review_hard_days = models.PositiveSmallIntegerField(
        default=1,
        help_text="Days until next review after marking a flashcard Hard.",
    )
    review_session_size = models.PositiveSmallIntegerField(
        default=20,
        help_text="Max cards per Review due session (0 = all due cards).",
    )
    best_streak = models.PositiveIntegerField(
        default=0,
        help_text="Longest streak achieved.",
    )
    streak = models.PositiveIntegerField(
        default=0,
        help_text=(
            "Current consecutive days with study activity (reading/vocab/writing)."
        ),
    )
    reading_speed_wpm = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=(
            "Last measured reading speed (words per minute), e.g. from skills lesson."
        ),
    )

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    @property
    def level_label(self) -> str:
        """Display label for placement / vocabulary level (Beginner, Standard, Advanced)."""
        return self.get_level_display()

    def __str__(self) -> str:
        return f"{self.user} · L{self.level}"
