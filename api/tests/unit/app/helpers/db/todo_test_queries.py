import unittest
from unittest.mock import Mock
EXCEPTED_ROUTE_RESPONSE = ""
FETCHALL_MOCKED_RETURN = [[1, "test"], [2, "test2"]]


class TestQueries(unittest.TestCase):
    def setUp(self):
        self.connection_mock = Mock(
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

    def test_query_commit(self):
        # TODO
        pass
