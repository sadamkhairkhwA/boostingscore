from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0009_userprofile_diagnostic_and_reviews"),
    ]

    operations = [
        migrations.AddField(
            model_name="vocabularyprogress",
            name="hard_easy_streak",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="Consecutive Easy ratings while the word is in the Hard words collection.",
            ),
        ),
        migrations.AddField(
            model_name="vocabularyprogress",
            name="is_hard_word",
            field=models.BooleanField(
                default=False,
                help_text="Keeps this word in the Hard words collection until the user clears it.",
            ),
        ),
    ]
