FROM python:3.9.7-alpine3.14

LABEL org.opencontainers.image.authors="benjamin.mathias@dataperl.com"
LABEL org.opencontainers.image.description="API to post comments about Rick & Morty universe"
LABEL org.opencontainers.image.documentation="https://github.com/benjmathias/jellyrick"
LABEL org.opencontainers.image.title="jellyrick-api"

# Copy source code to the container
COPY ./api /app
WORKDIR /app

COPY ./api/entrypoint/dev.entrypoint.sh /dev.entrypoint.sh
RUN chmod +x /dev.entrypoint.sh

RUN pip install --no-cache-dir -r /app/requirements.txt
