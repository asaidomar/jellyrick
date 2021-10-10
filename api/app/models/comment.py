from pydantic import BaseModel


class Comment(BaseModel):
    content: str = "Nice comment update example !"
