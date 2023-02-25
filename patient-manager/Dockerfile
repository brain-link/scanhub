FROM python:3.10-slim-bullseye

# RUN pip install --upgrade pip
RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE false

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY app/ressources /ressources

RUN poetry install && rm -rf /root/.cache/pip

# WORKDIR /patient-manager
COPY . /app
