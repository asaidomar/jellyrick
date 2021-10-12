import os
from datetime import timedelta, datetime
from typing import Optional, Union

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from ..config import get_settings
from ..helpers.db.queries import AutonomousQuery
from ..models.token import TokenData
from ..models.user import UserInDB

settings = get_settings()
SECRET_KEY = settings.secret_key_db_hash
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
    scopes={
        "user": "User basic rights",
        "moderator": "Can update comment",
        "administrator": "All rights",
    },
)


def verify_password(plain_password, hashed_password):
    """
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Union[UserInDB, bool]:
    """
    :param username:
    :param password:
    :return:
    """
    user = AutonomousQuery.get_db_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_auth_data(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> dict:
    """
    :param security_scopes:
    :param token:
    :return:
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    # Handle logout (Redis should be used instead of a file)
    blacklist_file_path = "/tmp/jellyrick_blacklisted_tokens"
    if os.path.isfile(blacklist_file_path):
        with open(blacklist_file_path, "r") as blacklist_file:
            blacklisted_tokens = [line.rstrip("\n") for line in blacklist_file]
        if token in blacklisted_tokens:
            raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = AutonomousQuery.get_db_user(username=token_data.username)
    if user is None:
        raise credentials_exception

    if not [i for i in token_data.scopes if i in security_scopes.scopes]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return {"user": user, "token": token}


async def check_and_get_user_from_auth_data(current_auth_data):
    user = current_auth_data["user"]
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def secure_on_user_scope(
    current_auth_data: dict = Security(
        get_current_auth_data, scopes=["user", "moderator", "administrator"]
    )
) -> UserInDB:
    """
    :param current_auth_data:
    :return:
    """
    return await check_and_get_user_from_auth_data(current_auth_data)


async def secure_on_moderator_scope(
    current_auth_data: dict = Security(
        get_current_auth_data, scopes=["moderator", "administrator"]
    )
) -> str:
    """
    :param current_auth_data:
    :return:
    """
    return await check_and_get_user_from_auth_data(current_auth_data)


async def secure_on_admin_scope(
    current_auth_data: dict = Security(get_current_auth_data, scopes=["administrator"])
) -> str:
    """
    :param current_auth_data:
    :return:
    """
    return await check_and_get_user_from_auth_data(current_auth_data)


async def get_current_active_token(
    current_auth_data: dict = Security(
        get_current_auth_data, scopes=["user", "moderator", "administrator"]
    )
) -> str:
    """
    :param current_auth_data:
    :return:
    """
    return current_auth_data["token"]
