#!/usr/bin/env python3

""" USAGE: 'chmod +x write_from_web_to_json.py && ./write_from_web_to_json.py <OUTPUT_PATH>'"""

import json
import sys

import requests


def get_result_from_api(url: str, column_name: str) -> dict:
    """
    :param url: api url
    :param column_name: match a col in db
    :return: dictionary with fetched data
    """
    result = []
    pages_total_number = requests.get(url).json()["info"]["pages"]
    for i in range(pages_total_number):
        url_f = f"{url}?page={i + 1}"
        print(f"Fetching {url_f}")
        page_result = requests.get(url_f).json()["results"]
        result.extend([i["name"] for i in page_result])
    return {column_name: list(set(result))}


def get_and_write_char_episode_result(
    file_path: str, url: str, characters: list
) -> None:
    """
    !!! Not exhaustive (too much data)
    Write data from api to a csv file
    :param file_path: file path string
    :param url: api url
    :param characters: list of characters to fetch
    :return: None
    """
    result = {}
    for character in characters:
        url_f = f"{url}?name={character}"
        print(f"Fetching {url_f}")
        page_result = requests.get(url_f).json()["results"]
        page_result = page_result[0]["episode"]
        result[character] = []
        for url_linked_episode in page_result:
            result[character].append(requests.get(url_linked_episode).json()["name"])

    with open(f"{file_path}/episode_character_appearance.csv", "w") as rick_file:
        rick_file.write("episode,character\n")
        for character in result:
            for episode in result[character]:
                rick_file.write(f"{episode};{character}\n")


if __name__ == "__main__":
    FILE_PATH = sys.argv[1]
    FILE_PATH_EPISODE = f"{FILE_PATH}/rick_data_episode.json"
    FILE_PATH_CHARACTER = f"{FILE_PATH}/rick_data_character.json"

    BASE_API_URL = "https://rickandmortyapi.com/api"
    EPISODE_API_URL = f"{BASE_API_URL}/episode"
    CHARACTER_API_URL = f"{BASE_API_URL}/character"

    print("Fetching rick and morty data from web...")
    source = {
        "episode": {
            "file_path": FILE_PATH_EPISODE,
            "json_result": get_result_from_api(
                EPISODE_API_URL, column_name="episode_name"
            ),
        },
        "character": {
            "file_path": FILE_PATH_CHARACTER,
            "json_result": get_result_from_api(
                CHARACTER_API_URL, column_name="character_name"
            ),
        },
    }

    for entity in source:
        with open(source[entity]["file_path"], "w") as file:
            json_to_dump = {entity: source[entity]["json_result"]}
            json.dump(json_to_dump, file, indent=4)

    # Bonus step to populate "episode_character_appearance" table
    get_and_write_char_episode_result(
        FILE_PATH,
        CHARACTER_API_URL,
        source["character"]["json_result"]["character_name"],
    )
