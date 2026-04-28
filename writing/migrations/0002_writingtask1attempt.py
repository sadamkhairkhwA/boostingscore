from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("writing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WritingTask1Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_id", models.IntegerField()),
                ("question_type", models.CharField(max_length=50)),
                ("response_text", models.TextField()),
                ("word_count", models.IntegerField()),
                ("band_score", models.FloatField()),
                ("task_achievement", models.FloatField()),
                ("coherence_cohesion", models.FloatField()),
                ("lexical_resource", models.FloatField()),
                ("grammar_accuracy", models.FloatField()),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                ("feedback_json", models.JSONField(blank=True, default=dict)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-completed_at"]},
        ),
    ]
