from string import Template
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, LimitOffsetPage, paginate
from fastapi_pagination.bases import AbstractPage, T
from mysql.connector import MySQLConnection

from ..helpers.db.queries import DbQuery
from ..helpers.services.checkers import check_item_not_found
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /character                *********************** #
# *********************** GET /character/{character_id} *********************** #
# *********************** GET /character/limit-offset   *********************** #

QUERY_SELECT_CHARACTER = Template(
    """
    SELECT `character_name` FROM `character`
    WHERE `character_id` LIKE '$character_id_value';
    """
)

dec_dict = dict(
    tags=["character"],
    description="route to get character data from rick and morty universe",
)


@router.get("/character/limit-offset", response_model=LimitOffsetPage[str], **dec_dict)
@router.get("/character", response_model=Page[str], **dec_dict)
def character_list_route(
    connection: MySQLConnection = Depends(connect_to_database),
) -> AbstractPage[T]:
    """
    :param connection: db connection instance
    :return: json with character data
    """
    query_str = QUERY_SELECT_CHARACTER.substitute(
        character_id_value="%",
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/character/{character_id}", **dec_dict)
def character_unique_route(
    character_id: Optional[int],
    connection: MySQLConnection = Depends(connect_to_database),
) -> str:
    """
    :param character_id:
    :param connection: db connection instance
    :return: json with character data
    """
    query_str = QUERY_SELECT_CHARACTER.substitute(
        character_id_value=character_id,
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    check_item_not_found(db_result)
    return db_result[0][0]
