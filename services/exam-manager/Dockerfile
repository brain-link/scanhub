ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update \
    && apt-get -y install curl

# Copy pyproject file and poetry lock to root
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

# Copy code to app folder
COPY . /app/