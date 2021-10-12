import unittest
from unittest.mock import patch

from fastapi import FastAPI

from api.app.main import app, prefix, include_routers


class TestMain(unittest.TestCase):
    @patch("api.app.main.app.include_router")
    def testMain(self, include_router_patch):
        self.assertIsInstance(app, FastAPI)
        self.assertIsInstance(prefix, str)
        include_routers()
        self.assertTrue(include_router_patch.called)
