#!/usr/bin/env python3

""" USAGE:
- chmod +x insert_from_json_to_db.py
- ./insert_from_json_to_db.py <MYSQL_DATABASE> <MYSQL_USER> <MYSQL_PASSWORD> <MYSQL_HOSTNAME> <JSON_SOURCE_FILE_PATH>
"""

import glob
import json
import sys

import mysql.connector
from mysql.connector import Error, MySQLConnection


def create_connection(
    database: str, user_name: str, user_password: str, host_name: str
) -> MySQLConnection:
    """
    :param database:
    :param user_name:
    :param user_password:
    :param host_name:
    :return: connection instance of MySQLConnection
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            database=database,
            user=user_name,
            passwd=user_password,
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"Error MYSQL")
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection: MySQLConnection, query: str) -> None:
    """
    execute query to mysql db
    :param connection:
    :param query: sql query string
    :return:
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_entity(json_ent_key: str, source_data: dict, conn: MySQLConnection) -> None:
    """
    :param json_ent_key: match the mysql table
    :param source_data: data that will be inserted to the database
    :param conn:
    :return:
    """
    for col in source_data:
        entities = [f'("{i}"),\n' for i in source_data[col]]
        entities = "".join(entities).rstrip(",\n")
        create_episodes = f"""
        INSERT IGNORE INTO
          `{json_ent_key}` (`{col}`)
        VALUES
            {entities}
        """
        print(
            f"\n--- Data from json are being inserted to "
            f'MYSQL table "{json_ent_key}" and column "{col}"...'
        )
        execute_query(conn, create_episodes)


if __name__ == "__main__":
    MYSQL_DATABASE = sys.argv[1]
    MYSQL_USER = sys.argv[2]
    MYSQL_PASSWORD = sys.argv[3]
    MYSQL_HOSTNAME = sys.argv[4]
    JSON_SOURCE_FILE_PATH = sys.argv[5]
    my_conn = create_connection(
        MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOSTNAME
    )

    sources_json_data_path = glob.glob(f"{JSON_SOURCE_FILE_PATH}/*.json")
    sources_json = []
    for source_json_path in sources_json_data_path:
        with open(source_json_path) as json_file:
            sources_json.append(json.load(json_file))

    for source_json in sources_json:
        for entity in source_json:
            insert_entity(entity, source_json[entity], my_conn)
