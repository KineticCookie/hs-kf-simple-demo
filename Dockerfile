FROM python:3.8-slim

RUN pip install poetry

COPY . /app/

WORKDIR /app/

RUN poetry export -f requirements.txt > requirements.txt

RUN pip install -r requirements.txt