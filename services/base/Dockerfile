FROM python:3.13-slim-trixie

# Must match every service image's WORKDIR: scanhub-libraries is installed here as a local
# path dependency, and uv records its absolute source path, so a mismatched WORKDIR between
# this image and a service image forces uv to reinstall it instead of reusing this layer.
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Sync into the system site-packages so every service image built FROM this one
# inherits scanhub-libraries and its dependencies at the workspace-locked versions.
ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock ./
COPY services/base/shared_libs ./services/base/shared_libs
RUN uv sync --frozen --package scanhub-libraries --no-editable
