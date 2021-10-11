#!/usr/bin/env python3

""" USAGE:
- chmod +x metadata_write_from_web_to_json.py
- ./metadata_write_from_web_to_json.py <OUTPUT_PATH> <SEASON_TOTAL_NUMBER> <API_KEY_IMDB>
"""

import json
import sys

import requests


def get_from_imdb(
    api_base_url,
    api_key_imdb,
    imdb_rick_id,
    season_total_number,
    entity_key,
):
    entity = {entity_key: []}
    for season_number in range(1, int(season_total_number) + 1):
        url = f"{api_base_url}/{api_key_imdb}/{imdb_rick_id}/{season_number}"
        response_json = requests.get(url).json()
        for episode_data in response_json["episodes"]:
            entity[entity_key].append((episode_data["title"], episode_data[entity_key]))
    return entity


if __name__ == "__main__":
    API_BASE_URL = "https://imdb-api.com/en/API/SeasonEpisodes"
    IMDB_RICK_ID = "tt2861424"
    FILE_PATH = sys.argv[1]
    SEASON_TOTAL_NUMBER = sys.argv[2]
    API_KEY_IMDB = sys.argv[3]
    FILE_PATH_PLOT = f"{FILE_PATH}/rick_data_plot.json"
    FILE_PATH_THUMBNAIL = f"{FILE_PATH}/rick_data_image.json"

    source = [
        {
            "entity_name": "episode",
            "file_path": FILE_PATH_PLOT,
            "json_result": get_from_imdb(
                API_BASE_URL, API_KEY_IMDB, IMDB_RICK_ID, SEASON_TOTAL_NUMBER, "plot"
            ),
        },
        {
            "entity_name": "episode",
            "file_path": FILE_PATH_THUMBNAIL,
            "json_result": get_from_imdb(
                API_BASE_URL,
                API_KEY_IMDB,
                IMDB_RICK_ID,
                SEASON_TOTAL_NUMBER,
                "image",
            ),
        },
    ]

    for data in source:
        with open(data["file_path"], "w") as file:
            entity_name = data["entity_name"]
            json_to_dump = {entity_name: data["json_result"]}
            json.dump(json_to_dump, file, indent=4)

    print(
        f"Success: Plot and Thumbnail data has been fetched from imdb.com and wrote to json files :\n"
        f'- "{FILE_PATH_PLOT}"\n'
        f'- "{FILE_PATH_THUMBNAIL}"'
    )
