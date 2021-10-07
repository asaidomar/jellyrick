#!/bin/sh

API_LOG=${API_LOG:-"/var/log/api.log"}

uvicorn app.main:app --reload --host 0.0.0.0 --port "${PORT}"

# We never end the container
tail -f /dev/null
