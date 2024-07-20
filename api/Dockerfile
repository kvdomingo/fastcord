FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 120
ENV POETRY_NO_INTERACTION 1
ENV POETRY_CACHE_DIR "/var/cache/pypoetry"
ENV POETRY_HOME /etc/poetry
ENV PATH "$POETRY_HOME/bin:$PATH"

WORKDIR /app

ARG POETRY_VERSION=1.7.1

SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget && \
    curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
