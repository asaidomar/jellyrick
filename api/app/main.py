from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .helpers.errors.override_default import override_default_error_handling
from .routers import auth_router, episode_router, character_router, report_router
from .routers.comment import (
    get_comment_router,
    post_comment_router,
    delete_comment_router,
    update_comment_router,
)
from .routers.user import (
    get_user_router,
    post_user_router,
    delete_user_router,
    update_user_router,
)

app = FastAPI(
    title="JellyRick 🚀", description="API to post comments about Rick & Morty universe."
)
prefix = "/api/v1"


def include_routers():
    routers = [
        auth_router,
        get_comment_router,
        post_comment_router,
        delete_comment_router,
        update_comment_router,
        get_user_router,
        post_user_router,
        delete_user_router,
        update_user_router,
        episode_router,
        character_router,
        report_router,
    ]

    for router in routers:
        app.include_router(router.router, prefix=prefix)


include_routers()
override_default_error_handling(app)
add_pagination(app)
