python manage.py collectstatic --no-input
python manage.py migrate

waitress-serve --port=8000 djcrm.wsgi:application
