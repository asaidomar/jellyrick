import unittest
from unittest.mock import Mock

EXCEPTED_ROUTE_RESPONSE = {"result": ["episode1", "episode2"]}
FETCHALL_MOCKED_RETURN = [[1, "episode1"], [2, "episode2"]]


class TestEpisodeRoute(unittest.TestCase):
    def test_episode_route(self):
        from api.app.routers.episode_router import episode_route

        connection_mock = Mock(
            cursor=Mock(
                return_value=Mock(
                    __enter__=Mock(
                        return_value=Mock(
                            fetchall=Mock(return_value=FETCHALL_MOCKED_RETURN)
                        )
                    ),
                    __exit__=Mock(),
                )
            )
        )
        route_result = episode_route(connection_mock)
        self.assertEqual(route_result, EXCEPTED_ROUTE_RESPONSE)
