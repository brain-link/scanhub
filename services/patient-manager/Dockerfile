# FROM python:3.10-slim-bullseye
ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# ENV POETRY_VIRTUALENVS_CREATE false
# COPY ./requirements.txt /app/requirements.txt


COPY pyproject.toml poetry.lock ./
# COPY app/ressources /ressources

ENV POETRY_REQUESTS_TIMEOUT=100
RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

# RUN pip install -r /app/requirements.txt \
#     && rm -rf /root/.cache/pip

COPY . /app
