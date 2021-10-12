from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..auth.jwt import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_token,
)
from ..models.token import Token

router = APIRouter()


@router.post("/login", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """
    Login route for auth with JWT and OAuth2
    :param form_data:
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    for scope in form_data.scopes:
        if scope == "user":
            continue
        # We check db rights from db, we skip user scope because all users can request user permission
        if not getattr(user, scope):
            raise HTTPException(
                status_code=403, detail="You don't have enough permissions"
            )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", tags=["auth"])
def logout_route(token: str = Depends(get_current_active_token)) -> dict:
    """
    Logout route that blacklist the json web token
    :param token:
    :return:
    """
    with open("/tmp/jellyrick_blacklisted_tokens", "w") as blacklist_file:
        blacklist_file.write(f"{token}\n")
    return {"detail": "successfully logged out"}
