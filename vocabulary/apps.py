from django.apps import AppConfig


class VocabularyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vocabulary"

    def ready(self):
        import vocabulary.signals  # noqa: F401
