FROM python:3.10-slim-bullseye

# RUN pip install --upgrade pip
# RUN pip install poetry

WORKDIR /app

# ENV POETRY_VIRTUALENVS_CREATE false
COPY ./requirements.txt /app/requirements.txt

# COPY pyproject.toml poetry.lock ./
COPY app/ressources /ressources

# RUN poetry install && rm -rf /root/.cache/pip
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app
