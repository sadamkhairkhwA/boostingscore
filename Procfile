release: python manage.py migrate --noinput && python manage.py seed_words && python manage.py collectstatic --noinput
web: gunicorn boosting_score.wsgi --bind 0.0.0.0:$PORT --log-file - --timeout 300 --graceful-timeout 300 --workers 2
