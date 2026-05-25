#!/bin/sh
set -e

echo "Running migrations..."
/app/.venv/bin/python manage.py migrate --noinput

echo "Starting gunicorn..."
exec /app/.venv/bin/gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -