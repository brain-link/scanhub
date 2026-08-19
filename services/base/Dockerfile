FROM python:3.13-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY shared_libs ./shared_libs
RUN uv pip install --system ./shared_libs
