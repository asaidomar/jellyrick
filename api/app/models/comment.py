from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    content: str = "Nice comment update example !"
    new: Optional[bool] = True
    in_review: Optional[bool] = False
    rejected: Optional[bool] = False
    approved: Optional[bool] = False

    class Config:
        schema_extra = {"example": {"content": "Nice comment update example !"}}


class CommentPostResponse(BaseModel):
    info: str = "Comment has been successfully added to resource ? with id 1"
    comment_id: int = 1
