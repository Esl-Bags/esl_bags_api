#!/bin/sh

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn esl_bags.wsgi --bind=0.0.0.0:80