from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import secure_on_admin_scope
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import User

router = APIRouter()

# *********************** DELETE /user/{id} *********************** #
QUERY_DELETE_USER = Template(
    """
DELETE FROM `user`
WHERE `username` = '$username';
    """
)


@router.delete(
    "/user/{username}",
    tags=["user"],
    description="route to delete user data",
)
def user_delete_route(
    username: str,
    connection: MySQLConnection = Depends(connect_to_database),
    _: User = Depends(secure_on_admin_scope),
) -> dict:
    """
    :param username: username to delete
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with user data
    """
    query_str = QUERY_DELETE_USER.substitute(
        username=username,
    )
    DbQuery(connection, query_str).commit_query()
    return {"result": f"success: user with id {username} has been deleted"}
