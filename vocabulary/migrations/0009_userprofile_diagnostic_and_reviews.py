from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0008_typeitattempt_mode_nullable_scores"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="diagnostic_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="diagnostic_results",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="section_reviews",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
