from django.apps import AppConfig


class BoostingscoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boostingscore"
    label = "boostingscore"
    verbose_name = "Boosting Score"

    def ready(self) -> None:
        from . import signals  # noqa: F401
