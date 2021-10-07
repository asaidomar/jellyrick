#!/usr/bin/env python3

""" USAGE: 'chmod +x write_from_web_to_json.py && ./write_from_web_to_json.py <OUTPUT_PATH>'"""

import json
import sys

import requests


def get_result(url, column_name):
    result = []
    pages_total_number = requests.get(url).json()["info"]["pages"]
    for i in range(pages_total_number):
        page_result = requests.get(f"{url}?page={i + 1}").json()["results"]
        result.extend([i["name"] for i in page_result])
    return {column_name: result}


if __name__ == "__main__":
    FILE_PATH = sys.argv[1]
    FILE_PATH_EPISODE = f"{FILE_PATH}/rick_data_episode.json"
    FILE_PATH_CHARACTER = f"{FILE_PATH}/rick_data_character.json"

    BASE_API_URL = "https://rickandmortyapi.com/api"
    EPISODE_API_URL = f"{BASE_API_URL}/episode"
    CHARACTER_API_URL = f"{BASE_API_URL}/character"

    source = {
        "episode": {
            "file_path": FILE_PATH_EPISODE,
            "json_result": get_result(EPISODE_API_URL, column_name="name"),
        },
        "character": {
            "file_path": FILE_PATH_CHARACTER,
            "json_result": get_result(CHARACTER_API_URL, column_name="name"),
        },
    }

    print("Fetching rick and morty data from web...")
    for entity in source:
        with open(source[entity]["file_path"], "w") as file:
            json_to_dump = {entity: source[entity]["json_result"]}
            json.dump(json_to_dump, file, indent=4)
