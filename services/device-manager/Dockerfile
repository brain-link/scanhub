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

# Copy the workspace root and the shared library (both needed to resolve this
# member from the shared lockfile) plus this service's own pyproject.toml
COPY pyproject.toml uv.lock ./
COPY services/base/shared_libs ./services/base/shared_libs
COPY services/device-manager/pyproject.toml ./services/device-manager/pyproject.toml

# Install dependencies for this workspace member only. scanhub-libraries (and its
# transitive deps, e.g. fastapi) are already installed in the base image at the exact
# versions locked here, so this only adds what's specific to device-manager.
RUN uv sync --frozen --package scanhub-device-manager --no-install-project --no-editable

# Copy the rest of the app
COPY services/device-manager/app ./app

# Set PYTHONPATH to include app/
ENV PYTHONPATH=/

# Start the app using uvicorn
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
