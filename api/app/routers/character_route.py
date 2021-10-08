from typing import List

from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()
CHARACTER_TABLE = "character"
QUERY_SELECT_CHARACTER = f"SELECT * FROM `{CHARACTER_TABLE}`"


class CharacterResult(BaseModel):
    result: List[str] = [
        "80's snake",
        "Abadango Cluster Princess",
        "Abradolf Lincler",
        "Accountant dog",
    ]


@router.get("/character", response_model=CharacterResult, tags=["get"])
def character_route(connection: MySQLConnection = Depends(connect_to_database)) -> dict:
    """
    route to get character data from rock and morty universe\n
    :param connection: (internal) dependency injection for db connection\n
    :return: json with character data\n
    """
    with connection.cursor() as cursor:
        cursor.execute(QUERY_SELECT_CHARACTER)
        character_list = [i[1] for i in cursor.fetchall()]
    return {"result": character_list}
