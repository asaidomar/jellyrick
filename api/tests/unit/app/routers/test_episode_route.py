import unittest

from api.app.routers.episode_route import episode_route


class TestEpisodeRoute(unittest.TestCase):
    def test_episode_route(self):
        route_result = episode_route()
        self.assertEqual(route_result, {})
