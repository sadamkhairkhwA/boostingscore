from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0015_userprofile_speaking_ai_notice_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="placement_results",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="placement_taken_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
