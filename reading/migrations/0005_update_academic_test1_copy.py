from django.db import migrations


def update_test1_copy(apps, schema_editor):
    ReadingTest = apps.get_model("reading", "ReadingTest")
    ReadingTest.objects.filter(number=1).update(
        title="Test 1 · Roman concrete, flexible work & bilingualism",
        description=(
            "Three academic passages — Roman materials science, workplace flexibility research, "
            "and the cognitive study of bilingualism."
        ),
    )


def revert_test1_copy(apps, schema_editor):
    ReadingTest = apps.get_model("reading", "ReadingTest")
    ReadingTest.objects.filter(number=1).update(
        title="Test 1 · Services, Travel & Bilingualism",
        description=(
            "Three authentic passages — library notices, workplace flexibility, "
            "and an academic article on bilingualism."
        ),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("reading", "0004_seed_academic_tests_2_6"),
    ]

    operations = [
        migrations.RunPython(update_test1_copy, revert_test1_copy),
    ]
