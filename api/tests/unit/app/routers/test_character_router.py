import unittest
from unittest.mock import patch, MagicMock


class TestCharacterRoute(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()

    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    def test_character_unique_route(self, commit_query_patch):
        from api.app.routers.character_router import character_unique_route

        excepted = "I want this return"
        commit_query_patch.return_value = [["I want this return"]]

        route_result = character_unique_route(self.connection_mock)
        self.assertEqual(route_result, excepted)
