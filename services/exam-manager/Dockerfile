FROM python:3.10-slim-bullseye

WORKDIR /app

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update \
    && apt-get -y install curl

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/