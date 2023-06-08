FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root && rm -rf /root/.cache/pip

#RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/