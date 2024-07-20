#!/bin/bash

set -euxo pipefail

poetry install --no-root
poetry run python manage.py migrate
poetry run python manage.py createsuperuser --noinput || true

exec poetry run python manage.py runserver 0.0.0.0:8000
