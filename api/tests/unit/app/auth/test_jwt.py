import unittest
from unittest.mock import patch, MagicMock, Mock


class TestJwtRoute(unittest.TestCase):
    def setUp(self):
        self.connection_mock = MagicMock()

    @patch("api.app.auth.jwt.verify_password")
    @patch("api.app.helpers.db.queries.AutonomousQuery.get_db_user")
    def test_jwt_authenticate_user_case_get_db_fail(self, get_db_user_patch, _):
        from api.app.auth.jwt import authenticate_user
        get_db_user_patch.return_value = False
        func_return = authenticate_user("fake_username", "fake_password")
        self.assertFalse(func_return)

    @patch("api.app.auth.jwt.verify_password")
    @patch("api.app.helpers.db.queries.AutonomousQuery.get_db_user")
    def test_jwt_authenticate_user_case_verify_password_fail(self, _, verify_password_patch):
        from api.app.auth.jwt import authenticate_user
        verify_password_patch.return_value = False
        func_return = authenticate_user("fake_username", "fake_password")
        self.assertFalse(func_return)
