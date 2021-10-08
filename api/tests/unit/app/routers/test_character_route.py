import unittest
from unittest.mock import Mock

EXCEPTED_ROUTE_RESPONSE = {"result": ["character1", "character2"]}
FETCHALL_MOCKED_RETURN = [[1, "character1"], [2, "character2"]]


class TestCharacterRoute(unittest.TestCase):
    def test_character_route(self):
        from api.app.routers.character_route import character_route

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
        route_result = character_route(connection_mock)
        self.assertEqual(route_result, EXCEPTED_ROUTE_RESPONSE)
