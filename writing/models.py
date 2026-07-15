from django.db import models
from django.contrib.auth.models import User


class Essay(models.Model):
    TASK_CHOICES = [("1", "Task 1"), ("2", "Task 2")]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=1, choices=TASK_CHOICES)
    question = models.TextField()
    essay_text = models.TextField()
    word_count = models.IntegerField(default=0)
    band_score = models.FloatField(null=True, blank=True)
    feedback_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — Task {self.task_type} — Band {self.band_score}"


class WritingTask1Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    question_type = models.CharField(max_length=50)
    response_text = models.TextField()
    word_count = models.IntegerField()
    time_taken_seconds = models.IntegerField(default=0)
    band_score = models.FloatField()
    task_achievement = models.FloatField()
    coherence_cohesion = models.FloatField()
    lexical_resource = models.FloatField()
    grammar_accuracy = models.FloatField()
    annotated_text = models.TextField(blank=True, default="")
    completed_at = models.DateTimeField(auto_now_add=True)
    feedback_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return (
            f"{self.user.username} — Task1 Q{self.question_id} — "
            f"Band {self.band_score:.1f}"
        )


class WritingTask2Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    essay_type = models.CharField(max_length=50)
    response_text = models.TextField()
    word_count = models.IntegerField()
    time_taken_seconds = models.IntegerField(default=0)
    band_score = models.FloatField()
    task_response = models.FloatField()
    coherence_cohesion = models.FloatField()
    lexical_resource = models.FloatField()
    grammar_accuracy = models.FloatField()
    annotated_text = models.TextField(blank=True, default="")
    completed_at = models.DateTimeField(auto_now_add=True)
    feedback_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-completed_at"]


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.CharField(max_length=100)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson_id")


class LessonPracticeAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.CharField(max_length=100)
    attempt_number = models.PositiveIntegerField()
    response_text = models.TextField()
    word_count = models.PositiveIntegerField(default=0)
    ready = models.BooleanField(default=False)
    feedback_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "lesson_id", "attempt_number")


class SkillProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_id = models.CharField(max_length=100)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "skill_id")


class GrammarTopicProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.CharField(max_length=100)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "topic_id")
