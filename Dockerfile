FROM docker.cnarasouli.ir/backend/python:3.12.3-bullseye

ENV PYTHONBUFFERED=1
WORKDIR /app

RUN apt update -y && apt upgrade -y
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /app/
