FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip
ADD ./requirementes.txt ./
RUN pip install -r requirementes.txt
COPY shared_libs ./shared_libs
RUN pip install ./shared_libs