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

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Sync into the base image's system site-packages, alongside the pre-installed shared library
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# 1. Install dependencies only (cached well)
COPY pyproject.toml uv.lock ./
COPY services/orchestration-engine/pyproject.toml ./services/orchestration-engine/pyproject.toml
RUN uv sync --frozen --package scanhub-orchestration-engine --no-install-project --no-editable

# 2. Copy source
COPY services/orchestration-engine ./services/orchestration-engine

# 3. Install just this project (fast)
# --no-editable: this is a built image, not a live dev checkout — the bind-mounted
# volume at DAGSTER_HOME/app (see docker-compose.yml) is for editing app code, but an
# editable install here would point back into ./services/orchestration-engine, which
# that same bind mount overwrites at container start, breaking the import. Pick up code
# edits by rebuilding the image, not by relying on hot-reload of the installed package.
RUN uv sync --frozen --package scanhub-orchestration-engine --no-editable

# Dagster configuration
RUN mkdir -p $DAGSTER_HOME
COPY services/orchestration-engine/dagster.yaml $DAGSTER_HOME/dagster.yaml
COPY services/orchestration-engine/workspace.yaml $DAGSTER_HOME/workspace.yaml
