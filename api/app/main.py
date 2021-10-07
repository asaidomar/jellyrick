from fastapi import FastAPI

from .routers import episode_route, character_route

app = FastAPI()
prefix = "/api/v1"

app.include_router(episode_route.router, prefix=prefix)
app.include_router(character_route.router, prefix=prefix)
