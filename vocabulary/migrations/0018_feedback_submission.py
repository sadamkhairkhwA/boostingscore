import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0017_userprofile_pending_email"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackSubmission",
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
                ("email", models.EmailField(blank=True, default="", max_length=254)),
                (
                    "feedback_type",
                    models.CharField(
                        choices=[
                            ("bug", "Bug"),
                            ("suggestion", "Suggestion"),
                            ("other", "Something else"),
                        ],
                        default="suggestion",
                        max_length=20,
                    ),
                ),
                ("message", models.TextField()),
                (
                    "page_url",
                    models.URLField(blank=True, default="", max_length=500),
                ),
                ("user_agent", models.TextField(blank=True, default="")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="feedback_submissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="feedbacksubmission",
            index=models.Index(
                fields=["user", "-created_at"], name="vocab_fb_user_created_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="feedbacksubmission",
            index=models.Index(
                fields=["feedback_type", "-created_at"],
                name="vocab_fb_type_created_idx",
            ),
        ),
    ]
