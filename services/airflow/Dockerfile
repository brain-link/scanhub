# Use the official Airflow image as the base image
FROM apache/airflow:2.10.5-python3.10

# Switch to root user to install additional packages
USER root

# Copy the requirements.txt file into the container
COPY requirements.txt /requirements.txt

# Switch to the airflow user to install the additional packages
USER airflow

# Install the additional packages
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt
