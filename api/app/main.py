from fastapi import FastAPI

from .helpers.errors.override_default import override_default
from .routers import episode_router, character_router
from .routers.comment import (
    get_comment_router,
    post_comment_router,
    delete_comment_router,
    update_comment_router,
)

app = FastAPI(
    title="JellyRick 🚀", description="API to post comments about Rick & Morty universe."
)
prefix = "/api/v1"
override_default(app)


def include_routers():
    app.include_router(episode_router.router, prefix=prefix)
    app.include_router(character_router.router, prefix=prefix)

    # Comment routers
    app.include_router(get_comment_router.router, prefix=prefix)
    app.include_router(post_comment_router.router, prefix=prefix)
    app.include_router(delete_comment_router.router, prefix=prefix)
    app.include_router(update_comment_router.router, prefix=prefix)


include_routers()
