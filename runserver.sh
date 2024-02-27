#!/bin/sh
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn core.wsgi --bind=0.0.0.0:80