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
    author_id: str
    post_date: str
    post_id: str


class PostCreateResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    created_at: str
