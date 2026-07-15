from django.db import migrations, models


def copy_review_days_to_hours(apps, schema_editor):
    UserProfile = apps.get_model("vocabulary", "UserProfile")
    for profile in UserProfile.objects.all().only(
        "id",
        "review_hard_days",
        "review_easy_days",
    ):
        hard_hours = max(12, int(profile.review_hard_days or 1) * 24)
        easy_hours = max(12, int(profile.review_easy_days or 7) * 24)
        UserProfile.objects.filter(pk=profile.pk).update(
            review_hard_hours=hard_hours,
            review_good_hours=72,
            review_easy_hours=easy_hours,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0010_vocabularyprogress_hard_words"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="review_easy_hours",
            field=models.PositiveSmallIntegerField(default=168),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="review_good_hours",
            field=models.PositiveSmallIntegerField(default=72),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="review_hard_hours",
            field=models.PositiveSmallIntegerField(default=24),
        ),
        migrations.RunPython(copy_review_days_to_hours, migrations.RunPython.noop),
    ]
