FROM python:3.11-slim

WORKDIR /app

COPY . public_api/

WORKDIR ./public_api

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["alembic", "upgrade", "head"]
