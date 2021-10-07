from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection

from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()
QUERY_SELECT_EPISODE = "SELECT * FROM `episode`"


@router.get("/episode")
def episode_route(connection: MySQLConnection = Depends(connect_to_database)) -> dict:
    """
    route to get episode data from rock and morty universe\n
    :return: json with episode data\n
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY_SELECT_EPISODE)
        episode_list = [i[1] for i in cursor.fetchall()]

    return {
        "result": episode_list
    }
