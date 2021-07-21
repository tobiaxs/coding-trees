#!/bin/bash

set -e

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py collectstatic --noinput
python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8001
