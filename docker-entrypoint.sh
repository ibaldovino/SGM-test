#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Run translations
echo "Running translations"
python manage.py compilemessages

echo "Added admin"
python manage.py initadmin

# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:9990
gunicorn core.wsgi:application --bind 0.0.0.0:9990
