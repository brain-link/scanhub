ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

COPY . /app/