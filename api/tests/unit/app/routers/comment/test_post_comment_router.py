import unittest
from string import Template
from unittest.mock import patch, MagicMock


class TestPostCommentRouter(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()

    @patch("api.app.routers.comment.post_comment_router.COMMENT_TAG_MAPPING")
    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    def test_comment_post_route_logic(self, commit_query_patch, _):
        from api.app.routers.comment.post_comment_router import comment_post_route_logic
        from api.app.models.comment import Comment

        tag = "my_tag"
        comment_target_it = 42
        mocked_response = {
            "info": f"Comment has been successfully added to resource {tag} with id {comment_target_it}",
            "comment_id": 777,
        }

        settings = MagicMock()
        commit_query_patch.return_value = [[777]]

        route_result = comment_post_route_logic(
            Template(""),
            Comment(content=""),
            self.connection_mock,
            settings,
            tag,
            comment_target_it,
        )
        self.assertEqual(route_result, mocked_response)

    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    def test_comment_route_with_parameters(self, commit_query_patch):
        from api.app.routers.comment.post_comment_router import (
            comment_route_with_parameters,
        )

        fake_character_id = 1
        fake_episode_id = 1
        mocked_response = {
            "info": f"Comment has been successfully added to character "
            f"id {fake_character_id} and episode id {fake_episode_id}",
            "comment_id": 777,
        }

        excepted = mocked_response
        commit_query_patch.return_value = [[777]]

        route_result = comment_route_with_parameters(
            self.connection_mock, fake_episode_id, fake_character_id
        )
        self.assertEqual(route_result, excepted)
