FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction

COPY . /app/