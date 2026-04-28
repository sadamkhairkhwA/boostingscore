# Generated manually for academic reading tests

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_reading_test(apps, schema_editor):
    ReadingTest = apps.get_model("reading", "ReadingTest")
    ReadingTest.objects.get_or_create(
        number=1,
        defaults={
            "slug": "academic-1",
            "title": "Test 1 · Services, Travel & Bilingualism",
            "description": "Three authentic passages — library notices, workplace flexibility, and an academic article on bilingualism.",
            "is_live": True,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("reading", "0002_generalreadingarticle_generalreadingsummary_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReadingTest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.PositiveSmallIntegerField(unique=True)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                ("title", models.CharField(max_length=220)),
                ("description", models.TextField(blank=True)),
                ("is_live", models.BooleanField(default=False)),
            ],
            options={"ordering": ["number"]},
        ),
        migrations.CreateModel(
            name="ReadingTestResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveSmallIntegerField()),
                ("band", models.CharField(max_length=20)),
                ("time_taken_seconds", models.PositiveIntegerField(default=0)),
                ("part1_score", models.PositiveSmallIntegerField(default=0)),
                ("part2_score", models.PositiveSmallIntegerField(default=0)),
                ("part3_score", models.PositiveSmallIntegerField(default=0)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="reading.readingtest",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reading_test_results",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-completed_at"]},
        ),
        migrations.RunPython(seed_reading_test, migrations.RunPython.noop),
    ]
