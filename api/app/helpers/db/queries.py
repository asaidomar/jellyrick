from string import Template
from typing import Any, List, Tuple

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

    def commit_query(
        self, return_value: bool = False, last_return_value: bool = False
    ) -> List[Tuple]:
        """
        commit a query and get a result if return value True
        :param return_value:
        :param last_return_value:
        :return:
        """
        with self.__connection.cursor(buffered=True) as cursor:
            for ind, query in enumerate(self.__queries):
                try:
                    cursor.execute(query)
                    self.__connection.commit()
                    if return_value:
                        return cursor.fetchall()
                    if ind == len(self.__queries) and last_return_value:
                        return cursor.fetch()
                except MySQLError as e:
                    self.__connection.rollback()
                    raise e


# If an SQL request is used more than once,
# we should create an autonomous db query function here
class AutonomousQuery:
    @staticmethod
    def get_db_user(username: str) -> UserInDB:
        """
        get a user data from db
        :param username:
        :return:
        """
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
