from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.comment_schemas import CommentResponse


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=3)


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    title: str
    content: str
    author_id: int
    created_at: str
    id: int


class MultiplePostResponse(BaseModel):
    username: str
    title: str
    content: str
    created_at: str
    id: int


class MultiplePostFormat(BaseModel):
    number_of_posts: int
    posts: List[MultiplePostResponse]


class PostWithCommentsResponse(BaseModel):
    post: PostResponse
    post_comments: List[CommentResponse]
