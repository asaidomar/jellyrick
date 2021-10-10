from string import Template
from typing import Optional

from fastapi import Depends, APIRouter
from fastapi_pagination import LimitOffsetPage, Page, paginate
from mysql.connector import MySQLConnection

from ...auth.jwt import get_current_active_user
from ...config import Settings, get_settings
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import User

router = APIRouter()

# *********************** GET /comment              *********************** #
# *********************** GET /comment/{comment_id} *********************** #
# *********************** GET /comment/limit-offset *********************** #

QUERY_SELECT_COMMENT = Template(
    """
    SELECT `$comment_content_col_name` FROM `$comment_table_name`
    WHERE `$comment_id_col_name` LIKE '$comment_id_value';
    """
)

dec_dict = dict(
    tags=["comment"],
    description="route to get comment data from rock and morty universe",
)


@router.get("/comment/limit-offset", response_model=LimitOffsetPage[str], **dec_dict)
@router.get("/comment", response_model=Page[str], **dec_dict)
def comment_list_route(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
):
    """
    :param connection: db connection instance
    :param settings:
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_SELECT_COMMENT.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_id_value="%",
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/comment/{comment_id}", **dec_dict)
def comment_unique_route(
    comment_id: Optional[int],
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
) -> str:
    """
    :param comment_id:
    :param connection: db connection instance
    :param settings:
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_SELECT_COMMENT.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_id_value=comment_id,
    )
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return db_result[0][0]
