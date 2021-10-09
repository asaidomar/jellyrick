from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from app.config import Settings, get_settings
from app.helpers.db.queries import Query
from app.helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** GET /comment *********************** #
QUERY_GET_COMMENT_LIST = Template(
    "SELECT `$comment_content_col_name` FROM $comment_table_name"
)


@router.get(
    "/comment",
    tags=["comment"],
    description="route to get comment data about episode, character or character in episode of Rick and Morty",
)
def comment_get_route_list(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    """
    :param connection: db connection instance
    :param settings: settings from config.py file
    :return: json with comment data
    """
    query_str = QUERY_GET_COMMENT_LIST.substitute(
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_table_name=settings.table.names.comment,
    )
    query = Query(connection, query_str)
    db_result = query.commit_query(return_value=True)

    return {"result": [i[0] for i in db_result]}
