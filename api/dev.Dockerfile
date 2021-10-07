FROM python:3.9.7-alpine3.14

LABEL org.opencontainers.image.authors="benjamin.mathias@dataperl.com"
LABEL org.opencontainers.image.description="API to post comments about Rick & Morty universe"
LABEL org.opencontainers.image.documentation="https://github.com/benjmathias/jellyrick"
LABEL org.opencontainers.image.title="jellyrick-api"

# Copy source code to the container
COPY ./api /app
WORKDIR /app

COPY ./api/entrypoint/dev.entrypoint.sh /dev.entrypoint.sh
COPY ./api/entrypoint/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /dev.entrypoint.sh /wait-for-it.sh

# Initialize the db
RUN mkdir /db
COPY ./db/data_source/ /db/data_source
COPY ./db/script/ /db/script
RUN chmod +x /db/script/insert_from_json_to_db.py /db/script/write_from_web_to_json.py

RUN pip install --no-cache-dir -r /app/requirements.txt && apk add bash
