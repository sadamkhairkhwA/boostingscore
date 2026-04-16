# Generated manually for admin-managed IELTS workflow.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reading", "0005_remove_readingquestion_passage_ieltstestresult_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="IELTSTest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("test_number", models.IntegerField(unique=True)),
                ("topic", models.CharField(max_length=200)),
                ("band_range", models.CharField(max_length=20)),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("foundation", "Foundation"),
                            ("lower", "Lower"),
                            ("mid", "Mid"),
                            ("upper", "Upper"),
                            ("advanced", "Advanced"),
                        ],
                        max_length=20,
                    ),
                ),
                ("question_types", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("total_questions", models.IntegerField(default=40)),
                ("time_limit", models.IntegerField(default=60, help_text="Minutes")),
                ("is_active", models.BooleanField(default=True)),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["test_number"]},
        ),
        migrations.CreateModel(
            name="IELTSTestContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content_json", models.JSONField()),
                ("version", models.IntegerField(default=1)),
                ("is_current", models.BooleanField(default=True)),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="reading.ieltstest",
                    ),
                ),
            ],
            options={"ordering": ["-generated_at"]},
        ),
        migrations.DeleteModel(name="IELTSTestResult"),
        migrations.DeleteModel(name="ReadingAttempt"),
        migrations.CreateModel(
            name="IELTSTestResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.IntegerField(default=0)),
                ("total_questions", models.IntegerField(default=40)),
                ("time_seconds", models.IntegerField(default=0)),
                ("answers_json", models.JSONField(default=dict)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "student",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="reading.ieltstest",
                    ),
                ),
            ],
        ),
    ]
