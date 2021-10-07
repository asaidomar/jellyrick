import unittest
from unittest.mock import patch, MagicMock
from api.app.routers.character_route import character_route


class TestCharacterRoute(unittest.TestCase):
    def test_character_route(self):
        # from db.data_source import
        route_result = character_route()
        self.assertEqual(route_result, {})
