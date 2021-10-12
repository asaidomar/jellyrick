import tempfile
import itertools
import pyexcel
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from mysql.connector import MySQLConnection
from starlette.requests import Request

from ..auth.jwt import secure_on_admin_scope
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
    _: User = Depends(secure_on_admin_scope),
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
        csv_string += f'{comment_id},"{comment_content}"\n'

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


# *********************** GET /report/episode/csv       *********************** #
QUERY_SELECT_EPISODE = """
SELECT episode_id
FROM episode
ORDER BY episode_id;
    """

QUERY_SELECT_EPISODE_COMMENT_NUMBER = """
SELECT episode_id,COUNT(*)
FROM episode_comment
GROUP BY episode_id;
    """

QUERY_SELECT_REJECTED_EPISODE_COMMENT_NUMBER = """
SELECT episode_id, COUNT(*)
FROM episode_comment
WHERE comment_id IN (
    SELECT comment_id
    FROM comment
    WHERE rejected = 1
)
GROUP BY episode_id;
    """

QUERY_SELECT_AVERAGE_EPISODE_COMMENT_LENGTH = """
SELECT episode_id, AVG(CHAR_LENGTH(comment_content)) 'Average letters'
FROM comment
LEFT JOIN episode_comment ON
comment.comment_id = episode_comment.comment_id
GROUP BY episode_id;
    """


@router.get(
    "/report/episode/csv",
    tags=["report"],
    description="route to get comment data report in xls format",
)
def report_route(
    connection: MySQLConnection = Depends(connect_to_database),
    _: User = Depends(secure_on_admin_scope),
) -> FileResponse:
    """
    :param connection: db connection instance
    :param _: current user => enable auth for the route
    :return: json with comment data
    """
    # We get episode
    db_result = DbQuery(connection, QUERY_SELECT_EPISODE).commit_query(
        return_value=True
    )
    db_result_episode = [i[0] for i in db_result]

    # We get episode comment number
    db_result = DbQuery(connection, QUERY_SELECT_EPISODE_COMMENT_NUMBER).commit_query(
        return_value=True
    )
    ep_com_number_dict = {ep: number for ep, number in db_result}

    # We get rejected episode comment number
    db_result = DbQuery(
        connection, QUERY_SELECT_REJECTED_EPISODE_COMMENT_NUMBER
    ).commit_query(return_value=True)
    db_result_rejected_number = [i[1] for i in db_result]

    # We get average episode comment length
    db_result = DbQuery(
        connection, QUERY_SELECT_AVERAGE_EPISODE_COMMENT_LENGTH
    ).commit_query(return_value=True)
    db_result_average_episode_comment_length = {ep: number for ep, number in db_result}

    # We generate the csv from a string
    csv_string = "episode_id,total_comment,total_rejected_comment,average_episode_comment_length\n"
    for episode_id, rejected_number in itertools.zip_longest(
        db_result_episode, db_result_rejected_number
    ):
        csv_string += (
            f"{episode_id},"
            f"{ep_com_number_dict.get(episode_id)},"
            f"{rejected_number},"
            f"{db_result_average_episode_comment_length.get(episode_id)}\n"
        )

    tmp_path = tempfile.NamedTemporaryFile().name
    tmp_path_csv = f"{tmp_path}.csv"

    # We write the csv file
    with open(tmp_path_csv, "w") as f:
        f.write(csv_string)

    return FileResponse(
        path=tmp_path_csv, filename="episode-report.csv", media_type="text/csv"
    )
