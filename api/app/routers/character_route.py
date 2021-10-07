from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection

from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()
QUERY_SELECT_CHARACTER = "SELECT * FROM `character`"


@router.get("/character")
def character_route(connection: MySQLConnection = Depends(connect_to_database)) -> dict:
    """
    route to get character data from rock and morty universe\n
    :return: json with character data\n
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY_SELECT_CHARACTER)
        character_list = [i[1] for i in cursor.fetchall()]

    return {
        "result": character_list
    }
