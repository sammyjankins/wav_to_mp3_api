# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
WORKDIR /app
COPY . /app
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev \
        git \
        ffmpeg
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]