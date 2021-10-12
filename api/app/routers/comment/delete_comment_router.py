from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import secure_on_moderator_scope
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import User

router = APIRouter()

# *********************** DELETE /comment/{id} *********************** #
QUERY_DELETE_COMMENT = Template(
    """
DELETE FROM `comment`
WHERE `comment_id` = $comment_id;
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
    _: User = Depends(secure_on_moderator_scope),
) -> dict:
    """
    :param comment_id: comment_id to delete
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_DELETE_COMMENT.substitute(
        comment_id=comment_id,
    )
    DbQuery(connection, query_str).commit_query()

    return {"result": f"success: comment id {comment_id} has been deleted"}
