from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0013_word_synonyms"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="plan",
            field=models.CharField(default="free", max_length=32),
        ),
        migrations.CreateModel(
            name="DailyAiUsage",
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
                ("usage_date", models.DateField()),
                ("count", models.PositiveSmallIntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_ai_usage",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-usage_date"],
                "unique_together": {("user", "usage_date")},
            },
        ),
        migrations.CreateModel(
            name="AiUsageLog",
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
                ("feature", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ai_usage_logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["user", "-created_at"], name="vocab_ai_user_created_idx"),
                    models.Index(fields=["feature", "-created_at"], name="vocab_ai_feat_created_idx"),
                ],
            },
        ),
    ]
