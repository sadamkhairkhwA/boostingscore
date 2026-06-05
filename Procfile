web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn boosting_score.wsgi --log-file - --timeout 300 --graceful-timeout 300 --workers 2
