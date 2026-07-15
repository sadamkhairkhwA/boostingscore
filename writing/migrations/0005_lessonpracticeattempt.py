from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("writing", "0004_task2_lesson_skill_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonPracticeAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("lesson_id", models.CharField(max_length=100)),
                ("attempt_number", models.PositiveIntegerField()),
                ("response_text", models.TextField()),
                ("word_count", models.PositiveIntegerField(default=0)),
                ("ready", models.BooleanField(default=False)),
                ("feedback_json", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("user", "lesson_id", "attempt_number")},
            },
        ),
    ]
