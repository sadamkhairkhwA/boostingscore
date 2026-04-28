from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0007_customdeck_colour_customdeck_emoji_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="typeitattempt",
            name="mode",
            field=models.CharField(
                choices=[
                    ("definition", "Definition only"),
                    ("sentence", "Sentence only"),
                    ("both", "Definition + sentence"),
                ],
                db_index=True,
                default="both",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="typeitattempt",
            name="definition_score",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="typeitattempt",
            name="sentence_score",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
