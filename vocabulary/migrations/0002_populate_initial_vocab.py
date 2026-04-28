from django.db import migrations

from vocabulary.initial_vocab import bulk_create_words


def populate_words(apps, schema_editor):
    Word = apps.get_model("vocabulary", "Word")
    bulk_create_words(Word, skip_if_exists=True)


def unpopulate_words(apps, schema_editor):
    """Reverse is a no-op to avoid deleting user-added words."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("vocabulary", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_words, unpopulate_words),
    ]
