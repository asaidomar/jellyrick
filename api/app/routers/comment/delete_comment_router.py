from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import secure_on_moderator_scope
from ...config import Settings, get_settings
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import User

router = APIRouter()

# *********************** DELETE /comment/{id} *********************** #
QUERY_DELETE_COMMENT = Template(
    """
DELETE FROM `$comment_table_name`
WHERE `$comment_id_col_name` = $comment_id;
    """
)


@router.delete(
    "/comment/{id}",
    tags=["comment"],
    description="route to delete comment data",
)
def comment_delete_route(
    comment_id: int,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(secure_on_moderator_scope),
) -> dict:
    """
    :param comment_id: comment_id to delete
    :param connection: db connection instance
    :param settings: settings from config.py file
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_DELETE_COMMENT.substitute(
        comment_table_name=settings.table.names.comment,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_id=comment_id,
    )
    DbQuery(connection, query_str).commit_query()

    return {"result": f"success: comment id {comment_id} has been deleted"}
