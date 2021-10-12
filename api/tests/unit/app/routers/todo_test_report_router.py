import unittest
from unittest.mock import patch, MagicMock
from api.app.routers.report_router import report_route

EXCEPTED_ROUTE_RESPONSE = "I want this return"


class TestReportRoute(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()

    @patch("api.app.helpers.db.queries.DbQuery.commit_query")
    @patch("fastapi_pagination.paginate")
    def test_report_list_route(self, commit_query_patch, paginate_patch):
        from api.app.routers.report_router import report_route

        paginate_patch.return_value = MagicMock()
        commit_query_patch.return_value = "I want this return"

        route_result = report_route(self.connection_mock)
        self.assertEqual(route_result, EXCEPTED_ROUTE_RESPONSE)
