from fastapi import FastAPI

from .routers import status_route

app = FastAPI()
prefix = "/api/v1"

app.include_router(status_route.router, prefix=prefix)
