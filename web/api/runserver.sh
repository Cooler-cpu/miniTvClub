python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

celery -A django_app.celery worker -l info --loglevel=DEBUG &
celery -A django_app.celery beat -l info --loglevel=DEBUG &

python manage.py runserver