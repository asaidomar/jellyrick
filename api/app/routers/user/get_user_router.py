from typing import Optional

from fastapi import Depends, APIRouter
from fastapi_pagination import LimitOffsetPage, Page, paginate
from mysql.connector import MySQLConnection

from ...auth.jwt import secure_on_admin_scope
from ...helpers.db.queries import DbQuery, AutonomousQuery
from ...helpers.services.checkers import check_item_not_found
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.user import User, UserInDB

router = APIRouter()

# *********************** GET /user              *********************** #
# *********************** GET /user/{user_id} *********************** #
# *********************** GET /user/limit-offset *********************** #

QUERY_SELECT_USER = """
    SELECT `username` FROM `user`;
    """

dec_dict = dict(
    tags=["user"],
    description="route to get user data",
)


@router.get("/user/limit-offset", response_model=LimitOffsetPage[str], **dec_dict)
@router.get("/user", response_model=Page[str], **dec_dict)
def user_list_route(
    connection: MySQLConnection = Depends(connect_to_database),
    _: User = Depends(secure_on_admin_scope),
):
    """
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with user data
    """
    query_str = QUERY_SELECT_USER
    db_result = DbQuery(connection, query_str).commit_query(return_value=True)
    return paginate([i[0] for i in db_result])


@router.get("/user/{username}", **dec_dict, response_model=User)
def user_unique_route(
    username: Optional[str],
    _: User = Depends(secure_on_admin_scope),
) -> UserInDB:
    """
    :param username:
    :param _: current user => enable auth for the route
    :return: json with user data
    """
    user = AutonomousQuery.get_db_user(username)
    check_item_not_found(user)
    return user
