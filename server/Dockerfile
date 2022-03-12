FROM python:3.8-slim-buster

# RUN pip install --upgrade pip
RUN pip3 install poetry

ENV POETRY_VIRTUALENVS_CREATE false

WORKDIR /tmp

ADD pyproject.toml .
ADD poetry.lock .

RUN poetry install

WORKDIR /scanhub
