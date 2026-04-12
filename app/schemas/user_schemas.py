from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserPosts(BaseModel):
    title: str
    content: str
    id: int
    created_at: str


class UserResponseWithPosts(BaseModel):
    username: str
    id: int
    created_at: str
    posts: list[UserPosts]


class RegularUserResponse(BaseModel):
    username: str
    id: int
    created_at: str


class MultipleUserResponse(BaseModel):
    count: int
    users: list[RegularUserResponse]
