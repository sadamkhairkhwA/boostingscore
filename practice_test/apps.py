from django.apps import AppConfig
from django.db.backends.signals import connection_created


def _tune_sqlite(sender, connection, **kwargs):
    """Make SQLite resilient to concurrent writes (Railway runs many workers).

    - WAL journal mode lets reads run concurrently with a single writer.
    - busy_timeout makes a writer wait (here, 30s) for a lock instead of
      raising "database is locked" immediately.
    - synchronous=NORMAL is the safe, faster setting recommended with WAL.

    No-op for non-SQLite engines (e.g. Postgres via DATABASE_URL).
    """
    if connection.vendor != "sqlite":
        return
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA busy_timeout=30000;")


class PracticeTestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "practice_test"
    verbose_name = "Full Practice Test"

    def ready(self):
        connection_created.connect(_tune_sqlite)
