web: python manage.py migrate --settings=basecore.settings.production && gunicorn basecore.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 3
