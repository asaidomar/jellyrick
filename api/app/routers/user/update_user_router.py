from string import Template
from typing import Dict

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import get_password_hash, secure_on_admin_scope
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import UserPost, User

router = APIRouter()

# *********************** UPDATE /user   *********************** #
QUERY_UPDATE_USER_TPL = Template(
    """
INSERT INTO `user` (username, full_name, email, hashed_password, disabled, administrator, reviewer, moderator)
VALUES ('$username', '$full_name', '$email', '$hashed_password', 
        '$disabled', '$administrator', '$reviewer', '$moderator')
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name),email=VALUES(email),
            hashed_password=VALUES(hashed_password),disabled=VALUES(disabled),
            administrator=VALUES(administrator),reviewer=VALUES(reviewer),moderator=VALUES(moderator);
    """
)


@router.put(
    "/user",
    tags=["user"],
    description=f"route to update user data.",
)
def user_update_route(
    body: UserPost,
    connection: MySQLConnection = Depends(connect_to_database),
    _: User = Depends(secure_on_admin_scope),
) -> Dict[str, str]:
    """
    :param body:
    :param connection:
    :param _: current user => enable auth for the route
    :return:
    """
    get_query = QUERY_UPDATE_USER_TPL.substitute(
        username=body.content.username,
        full_name=body.content.full_name,
        email=body.content.email,
        hashed_password=get_password_hash(body.content.password1),
        disabled=int(body.content.disabled),
        administrator=int(body.content.administrator),
        reviewer=int(body.content.reviewer),
        moderator=int(body.content.moderator),
    )
    DbQuery(connection, get_query).commit_query()
    response = f"User has been successfully updated"
    return {"info": response}
