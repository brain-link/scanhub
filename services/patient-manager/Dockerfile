ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

# Set working directory inside container
WORKDIR /app

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update && apt-get -y install curl

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Sync into the base image's system site-packages, alongside the pre-installed shared library
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Copy uv files first to install dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies using uv. --frozen skips lock freshness validation, since that
# would otherwise require resolving the "shared" extra (scanhub-libraries), whose path
# source lives outside this build context; the base image already provides it.
RUN uv sync --frozen --no-install-project

# Copy the rest of the app
COPY . .

# Set PYTHONPATH to include app/
ENV PYTHONPATH=/

# Start the app using uvicorn
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8100"]
