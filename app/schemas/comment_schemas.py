from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    content: str
    created_at: str
    comment_id: str
    author_id: str
    post_id: str
