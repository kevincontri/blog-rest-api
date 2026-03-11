from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class CommentCreate(BaseModel):
    content: str

class UserResponse(BaseModel):
    username: str
    id: str
    created_at: str

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

class CommentResponse(BaseModel):
    content: str
    created_at: str
    comment_id: str
    author_id: str
    post_id: str

class LoginRequest(BaseModel):
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
