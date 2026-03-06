#!/bin/bash
# Fix migration order safely
python manage.py migrate Auth 0001_initial --fake
python manage.py migrate admin 0001_initial --fake

# Apply any remaining migrations
python manage.py migrate

# Start the server
gunicorn CMSoloilepu.wsgi:application --bind 0.0.0.0:$PORT