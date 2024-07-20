#!/bin/bash

set -euxo pipefail

poetry install --no-root

exec poetry run python manage.py runserver 0.0.0.0:8000
