#!/bin/sh

python manage.py migrate

gunicorn slack_bot.wsgi:application --bind 0.0.0.0:8000

# exec "$@"