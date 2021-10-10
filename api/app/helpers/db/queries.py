from string import Template
from typing import Any

from mysql.connector import MySQLConnection, Error as MySQLError

from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import UserInDB


class DbQuery:
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


# If an SQL request is used more than once,
# we should create an autonomous db query function here
class AutonomousQuery:
    @staticmethod
    def get_db_user(username: str):
        query_str = Template(
            """
    SELECT username, full_name, email, hashed_password, disabled, administrator, reviewer, moderator 
    FROM user 
    WHERE username = '$user';
            """
        ).substitute(user=username)

        res = DbQuery(connect_to_database(), query_str).commit_query(return_value=True)[
            0
        ]
        if res:
            return UserInDB(
                username=res[0],
                full_name=res[1],
                email=res[2],
                hashed_password=res[3],
                disabled=res[4],
                administrator=res[5],
                reviewer=res[6],
                moderator=res[7],
            )
