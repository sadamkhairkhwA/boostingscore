from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("writing", "0003_writingtask1attempt_time_and_annotated"),
    ]

    operations = [
        migrations.CreateModel(
            name="WritingTask2Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_id", models.IntegerField()),
                ("essay_type", models.CharField(max_length=50)),
                ("response_text", models.TextField()),
                ("word_count", models.IntegerField()),
                ("time_taken_seconds", models.IntegerField(default=0)),
                ("band_score", models.FloatField()),
                ("task_response", models.FloatField()),
                ("coherence_cohesion", models.FloatField()),
                ("lexical_resource", models.FloatField()),
                ("grammar_accuracy", models.FloatField()),
                ("annotated_text", models.TextField(blank=True, default="")),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                ("feedback_json", models.JSONField(blank=True, default=dict)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-completed_at"]},
        ),
        migrations.CreateModel(
            name="LessonProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("lesson_id", models.CharField(max_length=100)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"unique_together": {("user", "lesson_id")}},
        ),
        migrations.CreateModel(
            name="SkillProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("skill_id", models.CharField(max_length=100)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"unique_together": {("user", "skill_id")}},
        ),
    ]
