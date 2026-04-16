from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boostingscore", "0001_initial_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="review_easy_days",
            field=models.PositiveSmallIntegerField(
                default=7,
                help_text="Days until next review after marking a flashcard Easy.",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="review_hard_days",
            field=models.PositiveSmallIntegerField(
                default=1,
                help_text="Days until next review after marking a flashcard Hard.",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="review_session_size",
            field=models.PositiveSmallIntegerField(
                default=20,
                help_text="Max cards per Review due session (0 = all due cards).",
            ),
        ),
    ]
