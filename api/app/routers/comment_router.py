from string import Template

from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from ..config import Settings, get_settings
from ..helpers.db.queries import Query
from ..helpers.services.mysql_connect_service import connect_to_database

router = APIRouter()

# *********************** POST /comment *********************** #

QUERY_POST_COMMENT_TPL = Template(
    """
INSERT INTO `$comment_table_name` ($comment_content_col_name) VALUES ('$comment_content');
SET @last_id_in_comment = LAST_INSERT_ID();

INSERT INTO `$comment_linked_tag_table_name` ($comment_id_col_name, $comment_linked_tag_col_name) 
VALUES (@last_id_in_comment, $comment_linked_tag_value);
    """
)


class CommentBody(BaseModel):
    content: str = "Nice comment example on episode !"


COMMENT_TAG_MAPPING = {
    "episode": {
        "linked_tag_table_name": get_settings().table.names.episode_comment,
        "linked_tag_col_name": get_settings().table.episode_comment_col_names.episode_id,
    },
    "character": {
        "linked_tag_table_name": get_settings().table.names.character_comment,
        "linked_tag_col_name": get_settings().table.character_comment_col_names.character_id,
    },
}


def comment_post_route_logic(
    body: CommentBody,
    connection: MySQLConnection,
    settings: Settings,
    tag: str,
    episode_id: int,
) -> dict[str, str]:
    insert_query = QUERY_POST_COMMENT_TPL.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_content=body.content,
        comment_id_col_name=settings.table.comment_col_names.comment_id,
        comment_linked_tag_table_name=COMMENT_TAG_MAPPING[tag]["linked_tag_table_name"],
        comment_linked_tag_col_name=COMMENT_TAG_MAPPING[tag]["linked_tag_col_name"],
        comment_linked_tag_value=episode_id,
    )
    query = Query(connection, insert_query)
    query.commit_query()
    # TODO : change to comment_get_route when implemented
    response = {
        "info": f"Comment has been successfully added to resource {tag} with id {episode_id}"
    }
    response.update(comment_get_route_list(connect_to_database()))
    return response


# *********************** POST /comment/episode   *********************** #
# *********************** POST /comment/character *********************** #
route_path_list = [
    "/comment/episode/{episode_id}",
    "/comment/character/{character_id}",
]

for route_path in route_path_list:
    route_tag = route_path.split("/")[2]

    @router.post(
        route_path,
        tags=["comment"],
        description=f"route to post comment data about Rick and Morty.",
    )
    def comment_route(
        body: CommentBody,
        episode_id: int,
        connection: MySQLConnection = Depends(connect_to_database),
        settings: Settings = Depends(get_settings),
    ) -> dict:
        response = comment_post_route_logic(
            body, connection, settings, route_tag, episode_id
        )
        return response


# *********************** POST /comment/?episode=1   *********************** #
# *********************** POST /comment/?character=1   *********************** #
# *********************** POST /comment/?episode=1&character=1   *********************** #

@router.post(
    "/comment",
    tags=["comment"],
    description=f"route to post comment data about Rick and Morty.",
)
def comment_route(
    body: CommentBody,
    episode_id: int = None,
    character_id: int = None,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    response = comment_post_route_logic(
        body, connection, settings, route_tag, episode_id
    )
    return response


# *********************** GET /comment *********************** #

QUERY_GET_COMMENT_LIST = Template(
    "SELECT `$comment_content_col_name` FROM $comment_table_name"
)


@router.get(
    "/comment",
    # response_model=CommentBody,
    tags=["comment"],
    description="route to get comment data about episode, character or character in episode of Rick and Morty",
)
def comment_get_route_list(
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = get_settings(),
) -> dict:
    """
    :param connection: db connection instance
    :param settings: settings from config.py file
    :return: json with comment data
    """
    query_str = QUERY_GET_COMMENT_LIST.substitute(
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_table_name=settings.table.names.comment,
    )
    query = Query(connection, query_str)
    db_result = query.commit_query(return_value=True)

    return {"result": [i[0] for i in db_result]}
