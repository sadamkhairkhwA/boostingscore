from django.db import models
from django.contrib.auth.models import User


class IELTSTestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.IntegerField()
    test_title = models.CharField(max_length=200)
    band = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=40)
    time_taken_secs = models.IntegerField(default=0)
    answers_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — Test {self.test_id} — {self.score}/40"


class ReadingAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=20, default="ielts")
    score = models.FloatField(null=True, blank=True)
    total_questions = models.IntegerField(default=40)
    correct_answers = models.IntegerField(default=0)
    time_taken_secs = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — {self.score}"


class GeneralReadingArticle(models.Model):
    TOPIC_CHOICES = [
        ("environment", "Environment"),
        ("health", "Health"),
        ("technology", "Technology"),
        ("society", "Society"),
        ("science", "Science"),
        ("business", "Business"),
        ("education", "Education"),
    ]
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    minutes = models.IntegerField(default=5)
    words = models.IntegerField(default=300)
    question_count = models.IntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    paragraphs = models.JSONField(default=list, blank=True)
    vocab = models.JSONField(default=list, blank=True)
    questions_json = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "topic", "title"]

    def __str__(self):
        return self.title


class GeneralReadingSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(GeneralReadingArticle, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=5)
    correct_answers = models.IntegerField(default=0)
    wpm = models.IntegerField(default=0)
    time_taken_secs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class GeneralReadingBookmark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(GeneralReadingArticle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "article"], name="general_reading_bookmark_unique"
            )
        ]
        ordering = ["-created_at"]


class GeneralReadingSummary(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        GeneralReadingArticle, on_delete=models.SET_NULL, null=True, blank=True
    )
    summary_text = models.TextField()
    feedback_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]


class ReadingTest(models.Model):
    """Catalogue row for fixed academic reading tests (seeded, not admin-edited yet)."""

    number = models.PositiveSmallIntegerField(unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    is_live = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Test {self.number}: {self.title}"


class ReadingTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_test_results")
    test = models.ForeignKey(ReadingTest, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveSmallIntegerField()
    band = models.CharField(max_length=20)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    part1_score = models.PositiveSmallIntegerField(default=0)
    part2_score = models.PositiveSmallIntegerField(default=0)
    part3_score = models.PositiveSmallIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    def duration_label(self) -> str:
        t = max(0, int(self.time_taken_seconds or 0))
        m, s = divmod(t, 60)
        if m and s:
            return f"{m} min {s:02d} sec"
        if m:
            return f"{m} min"
        return f"{s} sec"

    def duration_display_parts(self) -> tuple[str, str]:
        """(main, unit) for hub table — e.g. ('32', 'sec'), ('60', 'min')."""
        t = max(0, int(self.time_taken_seconds or 0))
        m, s = divmod(t, 60)
        if m and s:
            return (f"{m} min {s:02d}", "sec")
        if m:
            return (str(m), "min")
        return (str(s), "sec")

    @property
    def band_pill_modifier(self) -> str:
        """Suffix for art-band-pill--* classes on the tests hub."""
        raw = (self.band or "").strip()
        low = raw.lower()
        if "below" in low:
            return "red"
        try:
            val = float(raw)
        except ValueError:
            return "neutral"
        if val < 5.0:
            return "red"
        if val < 6.5:
            return "amber"
        if val < 8.0:
            return "blue"
        return "green"

    def __str__(self):
        return f"{self.user.username} — {self.test.slug} {self.score}/40"
