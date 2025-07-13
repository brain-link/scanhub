ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

# Set working directory inside container
WORKDIR /app

# Copy poetry files first to install dependencies
COPY pyproject.toml poetry.lock ./

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update && apt-get -y install curl

# Install poetry
RUN pip install poetry

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

# Copy the rest of the app
COPY . .

# Set PYTHONPATH to include app/
ENV PYTHONPATH=/

# Start the app using uvicorn
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8100"]
