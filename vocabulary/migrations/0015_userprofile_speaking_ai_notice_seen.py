from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0014_plan_and_ai_usage"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="speaking_ai_notice_seen",
            field=models.BooleanField(default=False),
        ),
    ]
