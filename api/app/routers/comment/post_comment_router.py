from string import Template

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection
from pydantic import BaseModel

from app.config import get_settings, Settings
from app.helpers.db.queries import Query
from app.helpers.services.mysql_connect_service import connect_to_database
from app.routers.comment.get_comment_router import comment_get_route_list

router = APIRouter()


class CommentBody(BaseModel):
    content: str = "Nice comment example on episode !"


# This enable two routes to be refactored ("/comment/episode" and "/comment/character")
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
    query_post_comment_tpl: Template,
    body: CommentBody,
    connection: MySQLConnection,
    settings: Settings,
    tag: str,
    episode_id: int,
) -> dict[str, str]:
    """
    Execute the insert query from query_post_comment_tpl and return the comment that was created
    :param query_post_comment_tpl:
    :param body:
    :param connection:
    :param settings:
    :param tag:
    :param episode_id:
    :return:
    """
    insert_query = query_post_comment_tpl.substitute(
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
QUERY_POST_COMMENT_TPL = Template(
    """
INSERT INTO `$comment_table_name` ($comment_content_col_name) VALUES ('$comment_content');
SET @last_id_in_comment = LAST_INSERT_ID();

INSERT INTO `$comment_linked_tag_table_name` ($comment_id_col_name, $comment_linked_tag_col_name) 
VALUES (@last_id_in_comment, $comment_linked_tag_value);
    """
)
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
        comment_target_id: int,
        connection: MySQLConnection = Depends(connect_to_database),
        settings: Settings = Depends(get_settings),
    ) -> dict:
        response = comment_post_route_logic(
            QUERY_POST_COMMENT_TPL,
            body,
            connection,
            settings,
            route_tag,
            comment_target_id,
        )
        return response


# *********************** POST /comment/?episode=1&character=1   *********************** #
QUERY_POST_COMMENT_CHAR_IN_EPISODE_TPL = Template(
    """
INSERT INTO `$comment_table_name` ($comment_content_col_name) VALUES ('$comment_content');
SET @last_id_in_comment = LAST_INSERT_ID();

INSERT INTO `$ep_char_app_table_name` (
`$ep_char_app_commment_episode_col_name`, 
`$ep_char_app_commment_character_col_name`, 
`$ep_char_app_comment_comment_col_name`
) 
VALUES ('$ep_char_app_episode_id', '$ep_char_app_character_id', @last_id_in_comment);
    """
)


@router.post(
    "/comment",
    tags=["comment"],
    description=f"route to post comment data about Rick and Morty.",
)
def comment_route_with_parameters(
    body: CommentBody,
    episode_id: int = None,
    character_id: int = None,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
) -> dict:
    get_query = QUERY_POST_COMMENT_CHAR_IN_EPISODE_TPL.substitute(
        comment_table_name=settings.table.names.comment,
        comment_content_col_name=settings.table.comment_col_names.comment_content,
        comment_content=body.content,
        ep_char_app_commment_episode_col_name=settings.table.episode_character_appearance_comment_col_names.episode,
        ep_char_app_commment_character_col_name=settings.table.episode_character_appearance_comment_col_names.character,
        ep_char_app_comment_comment_col_name=settings.table.episode_character_appearance_comment_col_names.comment_id,
        ep_char_app_table_name=settings.table.names.episode_character_appearance_comment,
        ep_char_app_episode_id=episode_id,
        ep_char_app_character_id=character_id,
    )

    Query(connection, get_query).commit_query()
    response = {
        "info": f"Comment has been successfully "
        f"added to character id {character_id} and episode id {episode_id}"
    }
    response.update(comment_get_route_list(connect_to_database()))
    return response
