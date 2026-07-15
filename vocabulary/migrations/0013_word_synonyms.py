from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0012_typeitattempt_custom_card"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="synonyms",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
