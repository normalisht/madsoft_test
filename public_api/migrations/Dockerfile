FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . public_api/
WORKDIR ./public_api

RUN pip install -r requirements.txt

CMD ["alembic", "upgrade", "head"]
