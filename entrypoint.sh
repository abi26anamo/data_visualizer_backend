#!/bin/sh

num_cores=$(nproc)
workers_num=$((2*num_cores+1))
runserver_command="gunicorn exante_data.wsgi:application --bind 0.0.0.0:8000 --reload --timeout 300 --workers $workers_num --threads 6 --error-logfile - --access-logfile - --capture-output --log-level debug"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
eval "$runserver_command"
