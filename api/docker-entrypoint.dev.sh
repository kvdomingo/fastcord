#!/usr/bin/env bash

set -euxo pipefail

uv sync --frozen
exec uv run fastapi dev --host 0.0.0.0 --port 8000 --reload
