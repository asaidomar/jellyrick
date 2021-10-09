from string import Template
from typing import List

from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from ..config import get_settings, Settings
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /character *********************** #

QUERY_SELECT_CHARACTER = Template(
    "SELECT `$character_name_col_name` FROM `$character_table_name`"
)


class CharacterResult(BaseModel):
    result: List[str] = [
        "80's snake",
        "Abadango Cluster Princess",
        "Abradolf Lincler",
        "Accountant dog",
    ]


@router.get(
    "/character",
    response_model=CharacterResult,
    tags=["get"],
    description="route to get character data from rock and morty universe",
)
def character_route(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    """
    # TODO use Query custom class
    :param connection: db connection instance
    :param settings:
    :return: json with character data
    """
    query_str = QUERY_SELECT_CHARACTER.substitute(
        character_table_name=settings.table.names.character,
        character_name_col_name=settings.table.character_col_names.character_name,
    )
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        character_list = [i[0] for i in cursor.fetchall()]
    return {"result": character_list}
