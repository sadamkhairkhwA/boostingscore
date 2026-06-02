from django.contrib.auth.models import User
from django.db import models


class TestSession(models.Model):
    """A single sitting of a full or part practice test."""

    KIND_LISTENING = "listening"
    KIND_READING = "reading"
    KIND_WRITING = "writing"
    KIND_SPEAKING = "speaking"
    KIND_FULL = "full"
    KIND_CHOICES = [
        (KIND_LISTENING, "Listening"),
        (KIND_READING, "Reading"),
        (KIND_WRITING, "Writing"),
        (KIND_SPEAKING, "Speaking"),
        (KIND_FULL, "Full IELTS Test"),
    ]

    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="practice_test_sessions"
    )
    kind = models.CharField(max_length=16, choices=KIND_CHOICES, db_index=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS
    )

    band_overall = models.FloatField(null=True, blank=True)

    # Per-section band scores; null while not yet attempted
    band_listening = models.FloatField(null=True, blank=True)
    band_reading = models.FloatField(null=True, blank=True)
    band_writing = models.FloatField(null=True, blank=True)
    band_speaking = models.FloatField(null=True, blank=True)

    # Raw payload from the section runners (writing feedback JSON, reading
    # answer arrays, etc.) so the results page can render rich detail later.
    raw = models.JSONField(default=dict, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "-started_at"]),
            models.Index(fields=["user", "kind"]),
        ]

    def __str__(self):
        return f"{self.user.username} — {self.get_kind_display()} — {self.band_overall or '—'}"

    @property
    def is_full(self) -> bool:
        return self.kind == self.KIND_FULL


class SpeakingResponse(models.Model):
    """A single speaking question answer: audio file + transcript + scores."""

    PART_CHOICES = [
        (1, "Part 1"),
        (2, "Part 2"),
        (3, "Part 3"),
    ]

    session = models.ForeignKey(
        TestSession, on_delete=models.CASCADE, related_name="speaking_responses"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="speaking_responses"
    )
    part = models.PositiveSmallIntegerField(choices=PART_CHOICES)
    question_index = models.PositiveSmallIntegerField()
    question_text = models.TextField()

    audio = models.FileField(upload_to="speaking_audio/", blank=True, null=True)
    transcript = models.TextField(blank=True)
    duration_seconds = models.FloatField(default=0)

    # Four IELTS speaking band sub-scores
    fluency = models.FloatField(null=True, blank=True)
    vocabulary = models.FloatField(null=True, blank=True)
    grammar = models.FloatField(null=True, blank=True)
    pronunciation = models.FloatField(null=True, blank=True)
    band = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    raw = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["session_id", "part", "question_index", "-created_at"]
        indexes = [
            models.Index(fields=["session", "part", "question_index"]),
        ]

    def __str__(self):
        return f"{self.user.username} — P{self.part}Q{self.question_index} — {self.band or '—'}"
