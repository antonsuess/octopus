FROM python:3.11-slim

WORKDIR octopus

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
