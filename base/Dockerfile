FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip
COPY shared_libs ./shared_libs
RUN pip install --upgrade build
RUN python3 -m build ./shared_libs
RUN pip install ./shared_libs