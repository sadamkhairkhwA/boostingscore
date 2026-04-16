# Removes reading dashboard models from state. DB may never have had these tables
# (e.g. DB only migrated through 0002), so DROP IF EXISTS is used.

from django.db import migrations


def _drop_reading_dashboard_tables(apps, schema_editor):
    connection = schema_editor.connection
    # Default Django table names for models created in 0003_reading_dashboard_models
    tables = (
        "reading_ieltsattempt",
        "reading_readingattempt",
        "reading_readingsession",
    )
    quoted = connection.ops.quote_name
    with connection.cursor() as cursor:
        for t in tables:
            if connection.vendor == "sqlite":
                cursor.execute(f"DROP TABLE IF EXISTS {quoted(t)}")
            else:
                cursor.execute(f"DROP TABLE IF EXISTS {quoted(t)} CASCADE")


class Migration(migrations.Migration):

    dependencies = [
        ("reading", "0003_reading_dashboard_models"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name="IELTSAttempt"),
                migrations.DeleteModel(name="ReadingAttempt"),
                migrations.DeleteModel(name="ReadingSession"),
            ],
            database_operations=[
                migrations.RunPython(
                    _drop_reading_dashboard_tables,
                    migrations.RunPython.noop,
                ),
            ],
        ),
    ]
