FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN apt -y update \
    &&python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt
