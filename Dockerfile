FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY main.py ./
RUN pip install --no-cache-dir .

CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 600 main:app
