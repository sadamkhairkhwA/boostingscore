from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary", "0008_customdeck_rename"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="antonyms",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="word",
            name="collocations",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="word",
            name="part_of_speech",
            field=models.CharField(blank=True, help_text="e.g. noun, verb (shown on word list).", max_length=64),
        ),
        migrations.AddField(
            model_name="word",
            name="synonyms",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="customcard",
            name="antonyms",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="customcard",
            name="collocations",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="customcard",
            name="part_of_speech",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="customcard",
            name="synonyms",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
