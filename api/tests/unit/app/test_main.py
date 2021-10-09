import unittest
from unittest.mock import patch


class TestMain(unittest.TestCase):
    @patch("api.app.main.app.include_router")
    def testMain(self, include_router_patch):
        from api.app.main import app, prefix, include_routers
        from fastapi import FastAPI

        self.assertIsInstance(app, FastAPI)
        self.assertIsInstance(prefix, str)
        include_routers()
        self.assertTrue(include_router_patch.called)
