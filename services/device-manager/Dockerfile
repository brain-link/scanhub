ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update \
    && apt-get -y install curl

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

COPY . /app/