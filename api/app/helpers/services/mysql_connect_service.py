import os

import mysql.connector
from mysql.connector.errors import InterfaceError
from ..errors.handle_exceptions import handle_exceptions


@handle_exceptions(
    error_code={"InterfaceError": 503},
    error_message={"InterfaceError": "Connection to MYSQL db failed"},
    exception_types=(InterfaceError,)
)
def connect_to_database():
    connection = mysql.connector.connect(user=os.environ.get("MYSQL_USER"),
                                         password=os.environ.get("MYSQL_PASSWORD"),
                                         host=os.environ.get("MYSQL_HOST"),
                                         database=os.environ.get("MYSQL_DB"))
    return connection
