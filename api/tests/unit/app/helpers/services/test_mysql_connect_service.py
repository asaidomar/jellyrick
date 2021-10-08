import unittest
from unittest.mock import patch


class TestCharacterRoute(unittest.TestCase):
    @patch("mysql.connector.connect")
    def testConnectToDatabase(self, connect_patch):
        from api.app.helpers.services.mysql_connect_service import connect_to_database
        from mysql.connector import MySQLConnection

        connect_patch.return_value = MySQLConnection()
        self.assertIsInstance(connect_to_database(), MySQLConnection)
