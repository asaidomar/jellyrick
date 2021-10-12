from string import Template
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, Page, paginate
from fastapi_pagination.bases import AbstractPage, T
from mysql.connector import MySQLConnection

from ..helpers.db.queries import DbQuery
from ..helpers.services.checkers import check_item_not_found
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /episode              *********************** #
# *********************** GET /episode/{episode_id} *********************** #
# *********************** GET /episode/limit-offset *********************** #

QUERY_SELECT_EPISODE = Template(
    """
    SELECT `episode_name` FROM `episode`
    WHERE `episode_id` LIKE '$episode_id_value';
    """
)

dec_dict = dict(
    tags=["episode"],
    description="route to get episode data from rick and morty universe",
)


@router.get("/episode/limit-offset", response_model=LimitOffsetPage[str], **dec_dict)
@router.get("/episode", response_model=Page[str], **dec_dict)
def episode_list_route(
    connection: MySQLConnection = Depends(connect_to_database),
) -> AbstractPage[T]:
    """
    List episodes of rick and morty
    :param connection: db connection instance
    :return: json with episode data
    """
    query_str = QUERY_SELECT_EPISODE.substitute(
        episode_id_value="%",
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/episode/{episode_id}", **dec_dict)
def episode_unique_route(
    episode_id: Optional[int],
    connection: MySQLConnection = Depends(connect_to_database),
) -> str:
    """
    get an episode name of rick and morty data based on its id
    :param episode_id:
    :param connection: db connection instance
    :return: json with episode data
    """
    query_str = QUERY_SELECT_EPISODE.substitute(
        episode_id_value=episode_id,
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    check_item_not_found(db_result)
    return db_result[0][0]
