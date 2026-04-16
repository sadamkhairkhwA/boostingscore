from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Tests are now managed via Django admin."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Tests are now managed via Django admin. "
                "Use /admin/ to create and publish tests."
            )
        )
