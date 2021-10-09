from typing import Any

from mysql.connector import MySQLConnection, Error as MySQLError


class Query:
    def __init__(self, connection: MySQLConnection, query: str) -> None:
        self.__connection = connection
        # Have fun ;)
        self.__queries = (
            [i for i in query.split(";") if i and not i.isspace()]
            if ";" in query
            else [query]
        )

    def commit_query(self, return_value: bool = False) -> Any:
        with self.__connection.cursor(buffered=True) as cursor:
            for query in self.__queries:
                try:
                    cursor.execute(query)
                    self.__connection.commit()
                    if return_value:
                        return cursor.fetchall()
                except MySQLError as e:
                    self.__connection.rollback()
                    raise e
