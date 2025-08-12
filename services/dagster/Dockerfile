ARG BASE_IMG=ghcr.io/brain-link/scanhub/scanhub-base:latest
FROM $BASE_IMG

# Install ps and pgrep
RUN apt-get update && apt-get install -y procps curl && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dagster/app


# Install git (needed for git+https requirements)
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME