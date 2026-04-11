from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    post_author: str
    title: str
    content: str
    author_id: int
    post_date: str
    post_id: int


class PostCreateResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
