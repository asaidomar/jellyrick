from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.helpers.db.queries import Query
from app.helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()


class CommentBody(BaseModel):
    content: str = "Nice comment update example !"


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
    body: CommentBody,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    """
    :param body: body with comment content that will be used to update a comment
    :param comment_id: comment_id to put
    :param connection: db connection instance
    :param settings: settings from config.py file
    :return: json with comment data
    """
    query_str = QUERY_PUT_COMMENT.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_content=body.content,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_id=comment_id,
    )
    Query(connection, query_str).commit_query()

    return {"result": f"success: comment id {comment_id} has been put"}
