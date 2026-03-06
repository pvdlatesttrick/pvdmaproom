FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/app/data/app.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

RUN mkdir -p /app/data

EXPOSE 10000

CMD gunicorn -b 0.0.0.0:${PORT:-10000} --timeout 120 --workers 1 "app.main:create_app()"
