from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0011_userprofile_review_hour_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="typeitattempt",
            name="custom_card",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="type_it_attempts",
                to="vocabulary.customcard",
            ),
        ),
        migrations.AddIndex(
            model_name="typeitattempt",
            index=models.Index(fields=["student", "custom_card"], name="vocabulary__student_8a1f2c_idx"),
        ),
    ]
