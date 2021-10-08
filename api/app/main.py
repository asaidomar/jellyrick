from fastapi import FastAPI

from .helpers.errors.override_default import override_default
from .routers import episode_route, character_route

app = FastAPI(
    title="JellyRick 🚀", description="API to post comments about Rick & Morty universe."
)
prefix = "/api/v1"
override_default(app)


def include_routers():
    app.include_router(episode_route.router, prefix=prefix)
    app.include_router(character_route.router, prefix=prefix)


include_routers()
