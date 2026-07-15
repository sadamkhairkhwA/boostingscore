from django.contrib.auth.models import User
from django.db import models


class ListeningPracticeAttempt(models.Model):
    """One completed 'Practice by question type' set, saved to the user's history."""

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listening_practice_attempts"
    )
    question_type = models.CharField(max_length=40)        # type slug, e.g. "matching"
    type_label = models.CharField(max_length=80, blank=True)
    set_id = models.CharField(max_length=80)               # which practice set
    set_title = models.CharField(max_length=160, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    answers_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def percent(self) -> int:
        return round(self.score / self.total * 100) if self.total else 0

    def __str__(self):
        return f"{self.student.username} — {self.question_type} {self.score}/{self.total}"


class ListeningTypeCycle(models.Model):
    """Tracks which practice sets a user has finished in the current cycle per type."""

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listening_type_cycles"
    )
    question_type = models.CharField(max_length=40)
    completed_set_ids = models.JSONField(default=list, blank=True)
    cycle_number = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("student", "question_type")]
        ordering = ["question_type"]

    def __str__(self):
        n = len(self.completed_set_ids or [])
        return f"{self.student.username} — {self.question_type} cycle {self.cycle_number} ({n} done)"
