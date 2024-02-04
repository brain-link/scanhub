FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /cartesian_reco_app

# Install curl to perform healthcheck, assume yes to all prompts
RUN apt-get -y update

COPY ./cartesian_reco_app/requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./cartesian_reco_app/