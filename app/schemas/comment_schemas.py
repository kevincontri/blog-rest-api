from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    content: str
    created_at: str
    comment_id: int
    author_id: int
    post_id: int
