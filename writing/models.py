from django.conf import settings
from django.db import models


class WritingQuestion(models.Model):
    TASK1 = "task1"
    TASK2 = "task2"
    TYPE_CHOICES = [
        (TASK1, "Task 1"),
        (TASK2, "Task 2"),
    ]

    TOPIC_ENVIRONMENT = "environment"
    TOPIC_HEALTH = "health"
    TOPIC_TECHNOLOGY = "technology"
    TOPIC_EDUCATION = "education"
    TOPIC_SOCIETY = "society"

    TOPIC_CHOICES = [
        (TOPIC_ENVIRONMENT, "Environment"),
        (TOPIC_HEALTH, "Health"),
        (TOPIC_TECHNOLOGY, "Technology"),
        (TOPIC_EDUCATION, "Education"),
        (TOPIC_SOCIETY, "Society"),
    ]

    LEVEL_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
    ]

    KIND_ANY = ""
    T1_CHART = "t1_chart"
    T1_TABLE = "t1_table"
    T1_PROCESS = "t1_process"
    T1_MAP = "t1_map"
    T2_OPINION = "t2_opinion"
    T2_DISCUSSION = "t2_discussion"
    T2_PROBLEM = "t2_problem"
    T2_ADVANTAGES = "t2_advantages"
    T2_TWO_PART = "t2_two_part"

    PROMPT_KIND_CHOICES = [
        (KIND_ANY, "Any style"),
        (T1_CHART, "Task 1 · Charts & graphs"),
        (T1_TABLE, "Task 1 · Tables"),
        (T1_PROCESS, "Task 1 · Process / diagram"),
        (T1_MAP, "Task 1 · Maps"),
        (T2_OPINION, "Task 2 · Opinion / agree–disagree"),
        (T2_DISCUSSION, "Task 2 · Discussion (both views)"),
        (T2_PROBLEM, "Task 2 · Problem & solution"),
        (T2_ADVANTAGES, "Task 2 · Advantages & disadvantages"),
        (T2_TWO_PART, "Task 2 · Two-part questions"),
    ]

    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    topic = models.CharField(max_length=32, choices=TOPIC_CHOICES)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    prompt_kind = models.CharField(
        max_length=16,
        choices=PROMPT_KIND_CHOICES,
        blank=True,
        default="",
        help_text="IELTS prompt style; empty = any (legacy).",
    )

    class Meta:
        ordering = ["topic", "level", "id"]

    def __str__(self) -> str:
        return f"{self.get_topic_display()} L{self.level} ({self.question_type})"


class WritingCoachingSession(models.Model):
    """In-progress 3-draft coaching flow before final Essay is created."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="writing_coaching_sessions",
    )
    writing_question = models.ForeignKey(
        WritingQuestion,
        on_delete=models.CASCADE,
        related_name="coaching_sessions",
    )
    draft_1 = models.TextField(blank=True)
    draft_2 = models.TextField(blank=True)
    round_1_feedback = models.JSONField(default=dict)
    round_2_feedback = models.JSONField(default=dict)
    # stage 1 = show draft 1 form; 2 = draft 2; 3 = draft 3 (final)
    stage = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Coach session {self.pk} user={self.student_id} stage={self.stage}"


class Essay(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="essays",
    )
    writing_question = models.ForeignKey(
        WritingQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="essays",
    )
    question = models.TextField(help_text="Snapshot of the prompt at submission time.")
    question_type = models.CharField(max_length=10, choices=WritingQuestion.TYPE_CHOICES)
    draft_1 = models.TextField(blank=True, help_text="First attempt (coaching flow).")
    draft_2 = models.TextField(blank=True, help_text="Second attempt (coaching flow).")
    coaching_journey = models.JSONField(
        default=dict,
        blank=True,
        help_text="AI coaching JSON per round (round1, round2, round3).",
    )
    student_answer = models.TextField(help_text="Final submitted text (draft 3 in coaching flow).")
    word_count = models.IntegerField()
    band_score = models.FloatField(null=True, blank=True)
    task_achievement_score = models.FloatField(null=True, blank=True)
    coherence_score = models.FloatField(null=True, blank=True)
    lexical_score = models.FloatField(null=True, blank=True)
    grammar_score = models.FloatField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    grammar_mistakes = models.TextField(blank=True)
    vocabulary_suggestions = models.TextField(blank=True)
    feedback_highlights = models.JSONField(
        default=dict,
        blank=True,
        help_text="issue_spans / strength_spans for highlighted final text display.",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"{self.student} essay @ {self.submitted_at:%Y-%m-%d %H:%M}"


class WordBankEntry(models.Model):
    """Per-user phrases saved from AI vocabulary suggestions."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_bank_entries",
    )
    essay = models.ForeignKey(
        Essay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="word_bank_entries",
    )
    phrase = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.phrase[:50]


class ParaphrasePractice(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="paraphrase_practices",
    )
    topic = models.CharField(max_length=32, blank=True)
    level = models.PositiveSmallIntegerField()
    source_text = models.TextField(blank=True, help_text="AI-generated text the student paraphrased.")
    input_text = models.TextField(help_text="Student paraphrase.")
    feedback = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Paraphrase L{self.level} @{self.created_at:%Y-%m-%d}"
