import tempfile

import pyexcel
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from mysql.connector import MySQLConnection
from starlette.requests import Request

from ..auth.jwt import get_current_active_user
from ..helpers.db.queries import DbQuery
from ..helpers.services.mysql_connect_service import connect_to_database
from ..models.user import User

router = APIRouter()

# *********************** GET /report/comment/csv       *********************** #
# *********************** GET /report/comment/xls       *********************** #

QUERY_SELECT_COMMENT = """
SELECT comment_id, comment_content
FROM comment;
    """


@router.get(
    "/report/comment/csv",
    tags=["report"],
    description="route to get comment data report in csv format",
)
@router.get(
    "/report/comment/xls",
    tags=["report"],
    description="route to get comment data report in xls format",
)
def report_route(
    request: Request = Request,
    connection: MySQLConnection = Depends(connect_to_database),
    _: User = Depends(get_current_active_user),
) -> FileResponse:
    """
    :param request:
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    db_result = DbQuery(connection, QUERY_SELECT_COMMENT).commit_query(
        return_value=True
    )
    csv_string = "comment_id,comment_content\n"
    for comment_id, comment_content in db_result:
        csv_string += f"{comment_id},{comment_content}\n"

    tmp_path = tempfile.NamedTemporaryFile().name
    tmp_path_csv = f"{tmp_path}.csv"

    # Write to CSV first
    with open(tmp_path_csv, "w") as f:
        f.write(csv_string)

    extension = request.url.path.split("/")[-1]
    if extension == "csv":
        return FileResponse(
            path=tmp_path_csv, filename="comment-report.csv", media_type="text/csv"
        )

    if extension == "xls":
        tmp_path = tempfile.NamedTemporaryFile().name
        tmp_path_xls = f"{tmp_path}.xls"
        pyexcel.save_as(file_name=tmp_path_csv, dest_file_name=tmp_path_xls)
        return FileResponse(
            path=tmp_path_xls,
            filename="comment-report.xls",
            media_type="application/vnd.ms-excel",
        )
