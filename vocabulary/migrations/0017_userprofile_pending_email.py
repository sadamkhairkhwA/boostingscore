from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0016_userprofile_placement_results"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="pending_email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="pending_email_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
