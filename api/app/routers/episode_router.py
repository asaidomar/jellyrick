from string import Template
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, Page, paginate
from mysql.connector import MySQLConnection

from ..config import get_settings, Settings
from ..helpers.db.queries import DbQuery
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /episode              *********************** #
# *********************** GET /episode/{episode_id} *********************** #
# *********************** GET /episode/limit-offset *********************** #

QUERY_SELECT_EPISODE = Template(
    """
    SELECT `$episode_name_col_name` FROM `$episode_table_name`
    WHERE `$episode_id_col_name` LIKE '$episode_id_value';
    """
)

dec_dict = dict(
    tags=["episode"],
    description="route to get episode data from rock and morty universe",
)


@router.get("/episode/limit-offset", response_model=LimitOffsetPage[str], **dec_dict)
@router.get("/episode", response_model=Page[str], **dec_dict)
def episode_list_route(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
):
    """
    :param connection: db connection instance
    :param settings:
    :return: json with episode data
    """
    query_str = QUERY_SELECT_EPISODE.substitute(
        episode_table_name=settings.table.names.episode,
        episode_name_col_name=settings.table.episode_col_names.episode_name,
        episode_id_col_name=settings.table.episode_col_names.episode_id,
        episode_id_value="%",
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/episode/{episode_id}", **dec_dict)
def episode_unique_route(
    episode_id: Optional[int],
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> str:
    """
    :param episode_id:
    :param connection: db connection instance
    :param settings:
    :return: json with episode data
    """
    query_str = QUERY_SELECT_EPISODE.substitute(
        episode_table_name=settings.table.names.episode,
        episode_name_col_name=settings.table.episode_col_names.episode_name,
        episode_id_col_name=settings.table.episode_col_names.episode_id,
        episode_id_value=episode_id,
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return db_result[0][0]
