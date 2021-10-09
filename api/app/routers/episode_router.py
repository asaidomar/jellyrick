from string import Template
from typing import List

from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from ..config import get_settings, Settings
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /episode *********************** #

QUERY_SELECT_EPISODE = Template("SELECT `$col_name` FROM `$table_name`")


class EpisodeResult(BaseModel):
    result: List[str] = [
        "A Rickle in Time",
        "Anatomy Park",
        "Auto Erotic Assimilation",
    ]


@router.get(
    "/episode",
    response_model=EpisodeResult,
    tags=["get"],
    description="route to get episode data from rock and morty universe",
)
def episode_route(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    """
    # TODO use Query custom class
    :param settings: settings from config.py file
    :param connection: db connection instance
    :return: json with episode data
    """
    query_str = QUERY_SELECT_EPISODE.substitute(
        table_name=settings.table.names.episode,
        col_name=settings.table.episode_col_names.episode_name,
    )

    with connection.cursor() as cursor:
        cursor.execute(query_str)
        episode_list = [i[0] for i in cursor.fetchall()]

    return {"result": episode_list}
