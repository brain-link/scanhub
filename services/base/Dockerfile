FROM python:3.13-slim-trixie

RUN pip install --upgrade pip
COPY shared_libs ./shared_libs
RUN pip install --upgrade build
RUN python3 -m build ./shared_libs
RUN pip install ./shared_libs