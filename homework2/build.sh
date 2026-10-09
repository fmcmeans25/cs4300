#!/usr/bin/env bash
# Render build script: exit on the first error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_demo

# Create an admin account from environment variables (skip if it already exists)
if [[ -n "$DJANGO_SUPERUSER_USERNAME" ]]; then
  python manage.py createsuperuser --no-input || true
fi