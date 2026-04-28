"""WSGI config for Boosting Score."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boosting_score.settings")

application = get_wsgi_application()
