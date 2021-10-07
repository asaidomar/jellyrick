import unittest

from fastapi import HTTPException

from api.app.helpers.errors.handle_exceptions import handle_exceptions


class MyCustomException(Exception):
    pass


class TestHandleExceptions(unittest.TestCase):
    def test_handle_exceptions(self):
        @handle_exceptions(
            error_code={"MyCustomException": 503},
            error_message={"MyCustomException": "test error"},
            exception_types=(MyCustomException,),
        )
        @handle_exceptions(
            error_code={"Test": 503},
            error_message={"Test": "hello error"},
            exception_types=(Exception,),
        )
        def test_func():
            raise MyCustomException

        self.assertRaises(HTTPException, test_func)
