from string import Template
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, LimitOffsetPage
from fastapi_pagination.paginator import paginate
from mysql.connector import MySQLConnection

from ..config import get_settings, Settings
from ..helpers.db.queries import DbQuery
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /character                *********************** #
# *********************** GET /character/{character_id} *********************** #
# *********************** GET /character/limit-offset   *********************** #

QUERY_SELECT_CHARACTER = Template(
    """
    SELECT `$character_name_col_name` FROM `$character_table_name`
    WHERE `$character_id_col_name` LIKE '$character_id_value';
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
    settings: Settings = Depends(get_settings),
):
    """
    :param connection: db connection instance
    :param settings:
    :return: json with character data
    """
    query_str = QUERY_SELECT_CHARACTER.substitute(
        character_table_name=settings.table.names.character,
        character_name_col_name=settings.table.character_col_names.character_name,
        character_id_col_name=settings.table.character_col_names.character_id,
        character_id_value="%",
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/character/{character_id}", **dec_dict)
def character_unique_route(
    character_id: Optional[int],
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> str:
    """
    :param character_id:
    :param connection: db connection instance
    :param settings:
    :return: json with character data
    """
    query_str = QUERY_SELECT_CHARACTER.substitute(
        character_table_name=settings.table.names.character,
        character_name_col_name=settings.table.character_col_names.character_name,
        character_id_col_name=settings.table.character_col_names.character_id,
        character_id_value=character_id,
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return db_result[0][0]
