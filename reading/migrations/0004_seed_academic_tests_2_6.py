# Generated manually — seed academic reading tests 2–6

from django.conf import settings
from django.db import migrations


def seed_tests(apps, schema_editor):
    ReadingTest = apps.get_model("reading", "ReadingTest")
    rows = [
        (
            2,
            "academic-2",
            "Test 2 · Urban Food, Postal Reform & Dark Matter",
            "Community gardens, hydroponics and market rules; the 1840 Penny Post; an academic article on dark matter.",
        ),
        (
            3,
            "academic-3",
            "Test 3 · Museums, Remote Learning & Circular Economy",
            "Museum visitor information; remote learning at universities; plastic waste and the circular economy.",
        ),
        (
            4,
            "academic-4",
            "Test 4 · Smart Cards, Vertical Farming & Decision-Making",
            "Public transport smart cards; vertical farming; psychology of decisions under uncertainty.",
        ),
        (
            5,
            "academic-5",
            "Test 5 · Workplace Wellness, Antibiotics & Pompeii",
            "Workplace wellness programmes; antibiotic resistance; preserving archaeological sites at Pompeii.",
        ),
        (
            6,
            "academic-6",
            "Test 6 · Community Energy, Printing & Medical AI",
            "Community renewable energy schemes; the history of the printing press; AI in medical diagnosis.",
        ),
    ]
    for number, slug, title, description in rows:
        ReadingTest.objects.update_or_create(
            number=number,
            defaults={
                "slug": slug,
                "title": title,
                "description": description,
                "is_live": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("reading", "0003_readingtest_readingtestresult"),
    ]

    operations = [
        migrations.RunPython(seed_tests, migrations.RunPython.noop),
    ]
