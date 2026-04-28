from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("writing", "0002_writingtask1attempt"),
    ]

    operations = [
        migrations.AddField(
            model_name="writingtask1attempt",
            name="annotated_text",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="writingtask1attempt",
            name="time_taken_seconds",
            field=models.IntegerField(default=0),
        ),
    ]
