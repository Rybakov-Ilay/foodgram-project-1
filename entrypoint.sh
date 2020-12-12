#!/bin/bash

set -e

echo 'running migrations'
python manage.py makemigrations
python manage.py migrate --noinput

echo 'collecting static'
python manage.py collectstatic --noinput

echo 'running server'
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000