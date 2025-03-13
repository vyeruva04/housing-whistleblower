release: python manage.py migrate && python manage.py createsuperuser --noinput
web: gunicorn housing_app.wsgi