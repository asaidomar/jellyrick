#!/usr/bin/env python3

""" USAGE:
- chmod +x insert_from_json_to_db.py
- ./insert_from_json_to_db.py <MYSQL_DATABASE> <MYSQL_USER> <MYSQL_PASSWORD> <JSON_SOURCE_FILE_PATH>
"""

import json
import sys
import glob

import mysql.connector
from mysql.connector import Error


def create_connection(host_name, database, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, database=database, user=user_name, passwd=user_password,
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"Error MYSQL")
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_entity(json_ent_key, source_data, conn):
    for col in source_data:
        entities = [f'("{i}"),\n' for i in source_data[col]]
        entities = "".join(entities).rstrip(",\n")
        create_episodes = f"""
        INSERT INTO
          `{json_ent_key}` (`{col}`)
        VALUES
            {entities}
        """
        print(f"\n--- Data from json are being inserted to "
              f"MYSQL table \"{json_ent_key}\" and column \"{col}\"...")
        execute_query(conn, create_episodes)


if __name__ == "__main__":
    MYSQL_DATABASE = sys.argv[1]
    MYSQL_USER = sys.argv[2]
    MYSQL_PASSWORD = sys.argv[3]
    JSON_SOURCE_FILE_PATH = sys.argv[4]
    my_conn = create_connection("127.0.0.1", MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)

    sources_json_data_path = glob.glob(f"{JSON_SOURCE_FILE_PATH}/*.json")
    sources_json = []
    for source_json_path in sources_json_data_path:
        with open(source_json_path) as json_file:
            sources_json.append(json.load(json_file))

    for source_json in sources_json:
        for entity in source_json:
            insert_entity(entity, source_json[entity], my_conn)
