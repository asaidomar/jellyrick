#!/usr/bin/env python3

""" USAGE:
- chmod +x insert_from_json_to_db.py
- ./insert_from_json_to_db.py <MYSQL_DATABASE> <MYSQL_USER> <MYSQL_PASSWORD> <JSON_SOURCE_FILE_PATH>
"""

import json
import sys

import mysql.connector
from mysql.connector import Error


def create_connection(host_name, database, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            database=database,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
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


def insert_entities(json_ent_key, conn):
    entities = [f"(\"{i}\"),\n" for i in json_rick_data[json_ent_key]]
    entities = "".join(entities).rstrip(",\n")
    create_episodes = f"""
    INSERT INTO
      `{json_ent_key}` (`name`)
    VALUES
        {entities}
    """
    execute_query(conn, create_episodes)


if __name__ == "__main__":
    MYSQL_DATABASE = sys.argv[1]
    MYSQL_USER = sys.argv[2]
    MYSQL_PASSWORD = sys.argv[3]
    JSON_SOURCE_FILE_PATH = sys.argv[4]
    my_conn = create_connection("127.0.0.1", MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)

    with open(JSON_SOURCE_FILE_PATH) as json_file:
        json_rick_data = json.load(json_file)

    for entity in ["episode", "character"]:
        insert_entities(entity, my_conn)
