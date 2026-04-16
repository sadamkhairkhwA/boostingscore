from django.contrib.auth.models import User
from django.db import models


class IELTSTest(models.Model):
    DIFFICULTY_FOUNDATION = "foundation"
    DIFFICULTY_LOWER = "lower"
    DIFFICULTY_MID = "mid"
    DIFFICULTY_UPPER = "upper"
    DIFFICULTY_ADVANCED = "advanced"
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_FOUNDATION, "Foundation"),
        (DIFFICULTY_LOWER, "Lower"),
        (DIFFICULTY_MID, "Mid"),
        (DIFFICULTY_UPPER, "Upper"),
        (DIFFICULTY_ADVANCED, "Advanced"),
    ]

    test_number = models.IntegerField(unique=True)
    topic = models.CharField(max_length=200)
    band_range = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    question_types = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_questions = models.IntegerField(default=40)
    time_limit = models.IntegerField(default=60, help_text="Minutes")
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["test_number"]

    def __str__(self):
        return f"Test {self.test_number} — {self.topic}"


class IELTSTestContent(models.Model):
    test = models.ForeignKey(IELTSTest, on_delete=models.CASCADE, related_name="contents")
    content_json = models.JSONField()
    version = models.IntegerField(default=1)
    is_current = models.BooleanField(default=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Test {self.test.test_number} v{self.version}"


class IELTSTestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(IELTSTest, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=40)
    time_seconds = models.IntegerField(default=0)
    answers_json = models.JSONField(default=dict)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.student.username} — Test {self.test.test_number} — "
            f"{self.score}/{self.total_questions}"
        )

    @property
    def percentage(self) -> float:
        if not self.total_questions:
            return 0.0
        return round((self.score / self.total_questions) * 100, 1)

    @property
    def band_estimate(self) -> str:
        pct = self.percentage
        if pct >= 90:
            return "8.5-9.0"
        if pct >= 80:
            return "7.5-8.0"
        if pct >= 70:
            return "6.5-7.0"
        if pct >= 60:
            return "5.5-6.0"
        return "5.0-5.5"
