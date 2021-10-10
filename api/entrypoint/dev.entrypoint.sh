#!/bin/sh

# Wait for db entrypoint (creation of tables from dump)
/wait-for-it.sh db:3306 -t 120

# Fetch json data about rick and morty universe from web to json files
# /db/script/write_from_web_to_json.py "/db/data_source"

# Insert data to the "db" container from files in last argument folder
# /db/script/insert_from_json_to_db.py "universe" "root" "root" "db" "/db/data_source"

uvicorn app.main:app --reload --host 0.0.0.0 --port "${API_EXPOSED_PORT}"

# We never end the container
tail -f /dev/null
