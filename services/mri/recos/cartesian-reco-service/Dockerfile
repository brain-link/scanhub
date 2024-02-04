FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# Install gdcm to fix dicom (add P10 header info) after it was created
RUN apt-get -y update \
    && apt-get -y install libgdcm-tools

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

COPY . /app/