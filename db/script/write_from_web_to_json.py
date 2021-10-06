#!/usr/bin/env python3

""" USAGE: 'chmod +x write_from_web_to_json.py && ./write_from_web_to_json.py <OUTPUT_FILE>'"""

import json
import sys

import requests

base_api_url = "https://rickandmortyapi.com/api"
episode_api_url = f"{base_api_url}/episode"
character_api_url = f"{base_api_url}/character"


def get_result(url):
    result = []
    pages_total_number = requests.get(url).json()["info"]["pages"]
    for i in range(pages_total_number):
        page_result = requests.get(f"{url}?page={i + 1}").json()["results"]
        result.extend([i["name"] for i in page_result])
    return result


json_result = {
    "episode": get_result(episode_api_url),
    "character": get_result(character_api_url),
}

with open(sys.argv[1], "w") as file:
    json.dump(json_result, file, indent=4)
