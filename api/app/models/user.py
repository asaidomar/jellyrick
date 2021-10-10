import random
import re
from typing import Optional

from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    administrator: Optional[bool] = None
    reviewer: Optional[bool] = None
    moderator: Optional[bool] = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    class Config:
        schema_extra = {
            "example": {
                "username": f"johndoe{str(random.getrandbits(64))[:4]}",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "disabled": False,
                "administrator": False,
                "reviewer": False,
                "moderator": False,
            }
        }


class UserInDB(User):
    hashed_password: str = "hashed_password"


class SubUserPost(User):
    password: str = "secure_password"
    password1: str = "Secure_password1"
    password2: str = "Secure_password1"

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password1" in values and v != values["password1"]:
            raise ValueError("passwords do not match")
        elif len(values["password1"]) < 8:
            raise ValueError("Make sure your password is at lest 8 letters")
        elif re.search("[0-9]", values["password1"]) is None:
            raise ValueError("Make sure your password has a number in it")
        elif re.search("[A-Z]", values["password1"]) is None:
            raise ValueError("Make sure your password has a capital letter in it")
        return v


class UserPost(BaseModel):
    content: Optional[SubUserPost] = None

    class Config:
        schema_extra = {
            "example": {
                "content": {
                    **User.Config.schema_extra["example"],
                    **{
                        "password1": "Secure_password1",
                        "password2": "Secure_password1",
                    },
                },
            }
        }
