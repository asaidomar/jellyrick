import unittest
from unittest.mock import patch, MagicMock


class TestEpisodeRoute(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()

    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    def test_episode_unique_route(self, commit_query_patch):
        from api.app.routers.episode_router import episode_unique_route

        excepted = "I want this return"
        commit_query_patch.return_value = [["I want this return"]]

        route_result = episode_unique_route(self.connection_mock)
        self.assertEqual(route_result, excepted)
