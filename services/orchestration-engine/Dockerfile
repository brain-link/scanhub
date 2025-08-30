ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

# Environment
ARG DAGSTER_HOME=/opt/dagster/dagster_home
ENV DAGSTER_HOME=$DAGSTER_HOME
ARG DATA_LAKE_DIRECTORY=/data
ENV DATA_LAKE_DIRECTORY=$DATA_LAKE_DIRECTORY

WORKDIR /opt/dagster/app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        procps curl git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install poetry

# 1. Install dependencies only (cached well)
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

# 2. Copy source
COPY . .

# 3. Install just this project (fast)
RUN poetry install --only-root --no-interaction

# Dagster configuration
RUN mkdir -p $DAGSTER_HOME
COPY dagster.yaml $DAGSTER_HOME/dagster.yaml
COPY workspace.yaml $DAGSTER_HOME/workspace.yaml