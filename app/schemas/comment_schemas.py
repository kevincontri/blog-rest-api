from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    username: str
    user_id: int
    content: str
    created_at: str
    comment_id: int
