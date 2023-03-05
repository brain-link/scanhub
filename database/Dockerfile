FROM python:3.10-slim-bullseye

# WORKDIR /app
WORKDIR /usr/app/src

# COPY ./requirements.txt /app/requirements.txt
COPY ./requirements.txt ./

# RUN pip install -r /app/requirements.txt \
RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip
    
# COPY . /app/

# RUN chmod +x scanhub_database_models.py
CMD ["python", "./scanhub_database_models.py"]