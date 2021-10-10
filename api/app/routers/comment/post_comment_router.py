from string import Template
from typing import Dict

from fastapi import Depends, APIRouter
from mysql.connector import MySQLConnection

from ...auth.jwt import get_current_active_user
from ...config import get_settings, Settings
from ...helpers.db.queries import DbQuery
from ...helpers.services.mysql_connect_service import connect_to_database
from ...models.comment import Comment
from ...models.user import User

router = APIRouter()

# Data to map resource type with matching MYSQL tables
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
    body: Comment,
    connection: MySQLConnection,
    settings: Settings,
    tag: str,
    episode_id: int,
    _: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """
    Execute the insert query from query_post_comment_tpl and return a message
    :param query_post_comment_tpl:
    :param body:
    :param connection:
    :param settings:
    :param tag:
    :param episode_id:
    :param _: current user => enable auth for the route
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
    query = DbQuery(connection, insert_query)
    query.commit_query()
    response = {
        "info": f"Comment has been successfully added to resource {tag} with id {episode_id}"
    }
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


@router.post(
    "/comment/episode/{episode_id}",
    tags=["comment"],
    description=f"route to post comment data about Rick and Morty episodes.",
)
def comment_route(
    body: Comment,
    target_id: int,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
) -> dict:
    """
    :param body:
    :param target_id:
    :param connection:
    :param settings:
    :param _: current user => enable auth for the route
    :return:
    """
    tag = "episode"
    response = comment_post_route_logic(
        QUERY_POST_COMMENT_TPL,
        body,
        connection,
        settings,
        tag,
        target_id,
    )
    return response


@router.post(
    "/comment/character/{character_id}",
    tags=["comment"],
    description=f"route to post comment data about Rick and Morty characters.",
)
def comment_route(
    body: Comment,
    target_id: int,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
) -> dict:
    """
    :param body:
    :param target_id:
    :param connection:
    :param settings:
    :param _: current user => enable auth for the route
    :return:
    """
    tag = "character"
    response = comment_post_route_logic(
        QUERY_POST_COMMENT_TPL,
        body,
        connection,
        settings,
        tag,
        target_id,
    )
    return response


# *********************** POST /comment/?episode=39&character=2   *********************** #
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
    "/comment/character-in-episode",
    tags=["comment"],
    description=f"route to post comment data about Rick and Morty character in episode.",
)
def comment_route_with_parameters(
    body: Comment,
    episode_id: int,
    character_id: int,
    connection: MySQLConnection = Depends(connect_to_database),
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_active_user),
) -> Dict[str, str]:
    """
    :param body:
    :param episode_id:
    :param character_id:
    :param connection:
    :param settings:
    :param _: current user => enable auth for the route
    :return:
    """
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
    DbQuery(connection, get_query).commit_query()
    response = (
        f"Comment has been successfully "
        f"added to character id {character_id} and episode id {episode_id}"
    )
    return {"info": response}
