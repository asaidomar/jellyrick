import unittest
from unittest.mock import patch, MagicMock


class TestDeleteUserRouter(unittest.TestCase):
    def setUp(self):
        self.username = "777"

    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    def test_delete_user_router(self, _):
        from api.app.routers.user.delete_user_router import user_delete_route
        excepted = {'result': 'success: user with id 777 has been deleted'}

        route_result = user_delete_route(self.username)
        self.assertEqual(route_result, excepted)
