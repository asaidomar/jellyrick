from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import secure_on_moderator_scope
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.comment import Comment
from ...models.user import User

router = APIRouter()

# *********************** PUT /comment/{id} *********************** #
QUERY_PUT_COMMENT = Template(
    """
UPDATE `comment`
SET `comment_content` = '$comment_content'
WHERE `comment_id` = '$comment_id';
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
    _: User = Depends(secure_on_moderator_scope),
) -> dict:
    """
    :param body: body with comment content that will be used to update a comment
    :param comment_id: comment_id to put
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    query_str = QUERY_PUT_COMMENT.substitute(
        comment_content=body.content,
        comment_id=comment_id,
    )
    DbQuery(connection, query_str).commit_query()

    return {"result": f"success: comment id {comment_id} has been put"}
