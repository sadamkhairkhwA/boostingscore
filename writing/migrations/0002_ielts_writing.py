from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("writing", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="WritingSubmission"),
        migrations.DeleteModel(name="WritingPrompt"),
        migrations.CreateModel(
            name="WritingQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_text", models.TextField()),
                (
                    "question_type",
                    models.CharField(
                        choices=[("task1", "Task 1"), ("task2", "Task 2")],
                        max_length=10,
                    ),
                ),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("environment", "Environment"),
                            ("health", "Health"),
                            ("technology", "Technology"),
                            ("education", "Education"),
                            ("society", "Society"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "level",
                    models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3")]),
                ),
            ],
            options={
                "ordering": ["topic", "level", "id"],
            },
        ),
        migrations.CreateModel(
            name="Essay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField()),
                (
                    "question_type",
                    models.CharField(
                        choices=[("task1", "Task 1"), ("task2", "Task 2")],
                        max_length=10,
                    ),
                ),
                ("student_answer", models.TextField()),
                ("word_count", models.IntegerField()),
                ("band_score", models.FloatField(blank=True, null=True)),
                (
                    "task_achievement_score",
                    models.FloatField(blank=True, null=True),
                ),
                ("coherence_score", models.FloatField(blank=True, null=True)),
                ("lexical_score", models.FloatField(blank=True, null=True)),
                ("grammar_score", models.FloatField(blank=True, null=True)),
                ("ai_feedback", models.TextField(blank=True)),
                ("grammar_mistakes", models.TextField(blank=True)),
                ("vocabulary_suggestions", models.TextField(blank=True)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="essays",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "writing_question",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="essays",
                        to="writing.writingquestion",
                    ),
                ),
            ],
            options={
                "ordering": ["-submitted_at"],
            },
        ),
        migrations.CreateModel(
            name="WordBankEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phrase", models.CharField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "essay",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="word_bank_entries",
                        to="writing.essay",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="word_bank_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
