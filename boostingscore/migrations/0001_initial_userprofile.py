from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def backfill_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("boostingscore", "UserProfile")
    for u in User.objects.all().iterator():
        UserProfile.objects.get_or_create(
            user=u,
            defaults={"level": 2, "placement_completed": True},
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "level",
                    models.PositiveSmallIntegerField(
                        choices=((1, "Beginner"), (2, "Standard"), (3, "Advanced")),
                        default=2,
                        help_text="Vocabulary deck level (1–3) from placement test.",
                    ),
                ),
                (
                    "placement_completed",
                    models.BooleanField(
                        default=False,
                        help_text="When False, user must complete placement before study areas.",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user profile",
                "verbose_name_plural": "user profiles",
            },
        ),
        migrations.RunPython(backfill_profiles, noop_reverse),
    ]
