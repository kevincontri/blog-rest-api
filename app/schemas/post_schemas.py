from pydantic import BaseModel
from typing import Optional, List


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    title: str
    content: str
    author_id: int
    created_at: str
    id: int


class PostCreateResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    
class MultiplePostResponse(BaseModel):
    username: str
    title: str
    content: str
    created_at: str
    id: int
    
class MultiplePostFormat(BaseModel):
    count: int
    posts: List[MultiplePostResponse]
