release: python manage.py migrate --noinput && python manage.py seed_words && python manage.py collectstatic --noinput
web: gunicorn boosting_score.wsgi --log-file - --timeout 300 --graceful-timeout 300 --workers 2
