from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import get_current_active_user
from ...config import Settings, get_settings
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.comment import Comment
from ...models.user import User

router = APIRouter()

# *********************** PUT /comment/{id} *********************** #
QUERY_PUT_COMMENT = Template(
    """
UPDATE `$comment_table_name`
SET `$comment_content_col_name` = '$comment_content'
WHERE `$comment_id_col_name` = '$comment_id';
    """
)


@router.put(
    "/comment/{id}",
    tags=["comment"],
    description="route to update comment data",
)
def comment_put_route(
    comment_id: int,
    body: Comment,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
) -> dict:
    """
    :param body: body with comment content that will be used to update a comment
    :param comment_id: comment_id to put
    :param connection: db connection instance
    :param settings: settings from config.py file
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_PUT_COMMENT.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_content=body.content,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_id=comment_id,
    )
    DbQuery(connection, query_str).commit_query()

    return {"result": f"success: comment id {comment_id} has been put"}
