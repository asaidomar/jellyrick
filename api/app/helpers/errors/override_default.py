from fastapi import FastAPI
from fastapi.responses import JSONResponse


def override_default_error_handling(app: FastAPI):
    # Override default Exception 500
    @app.exception_handler(Exception)
    async def http_exception_handler(_, exc):
        res = JSONResponse(
            {
                "detail": {
                    "code": 500,
                    "message": f"Internal Server Error : {type(exc).__name__} : {exc}",
                }
            },
            status_code=500,
        )
        return res
