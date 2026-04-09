from fastapi import FastAPI, HTTPException, Depends
from app.schemas import *
from app.database import init_db
from app.services import UserService, PostService, CommentService
from typing import List
from app.security.auth import create_access_token, get_current_user

app = FastAPI(
    title="Blog REST API",
    version="1.0",
    description="RESTful Blog API in Python using FastAPI and SQLite with JWT authentication, layered architecture, and role-based resource ownership.",
)


@app.on_event("startup")
async def startup_event():
    init_db()


"""User Endpoints"""


@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    service = UserService()
    user = service.create_user(data.username, data.password)
    return user.to_dict()


@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest):
    service = UserService()
    validate = service.verify_credentials(data.username, data.password)
    if validate == 1:
        raise HTTPException(status_code=401, detail="User not found")
    elif validate == 2:
        raise HTTPException(status_code=404, detail="Wrong password")
    else:
        token = create_access_token(validate[0]["id"])
        return {"access_token": token, "token_type": "bearer"}


@app.get("/users", response_model=List[UserResponse])
def display_all_users():
    service = UserService()
    return service.get_all_users()


@app.get("/users/{user_id}", response_model=UserResponse)
def display_user(user_id: str):
    service = UserService()
    user = service.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


"""Posts Endpoints"""


@app.post("/posts", response_model=PostCreateResponse)
def create_post(post: PostCreate, current_user_id: str = Depends(get_current_user)):
    service = PostService()
    post = service.create_post(post.title, post.content, current_user_id)
    if post:
        return post.to_dict()
    raise HTTPException(
        status_code=400, detail="Bad Request Body - Author ID not found"
    )


@app.get("/posts")
def get_posts(
    author_id: str | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    service = PostService()
    query = service.get_post_query(author_id, search, sort_by, page, limit)
    return query


@app.get("/posts/{post_id}", response_model=PostResponse)
def display_post(post_id: str):
    service = PostService()
    post = service.get_post(post_id)
    if post:
        return dict(post)
    raise HTTPException(status_code=404, detail="Post not found")


@app.patch("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: str, post: PostUpdate, current_user_id: str = Depends(get_current_user)
):
    service = PostService()
    updated_post = service.update_post(
        post_id, current_user_id, post.title, post.content
    )
    if updated_post:
        return dict(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}")
def delete_post(post_id: str, current_user_id: str = Depends(get_current_user)):
    service = PostService()
    post_deleted = service.delete_post(post_id, current_user_id)
    if post_deleted:
        return {"message": "Post Deleted Successfully"}
    raise HTTPException(status_code=404, detail="Post not found")


"""Comments Endpoints"""


@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user_id: int = Depends(get_current_user),
):
    service = CommentService()  # Add try-except for notFoundError.
    new_comment = service.create_comment(post_id, current_user_id, comment.content)
    if new_comment:
        return new_comment.to_dict()
    raise HTTPException(status_code=404, detail="User and/or post not found")


@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def display_comments_from_post(post_id: str):
    service = CommentService()
    comments = service.get_comments_from_post(post_id)
    if comments:
        return comments
    return []


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: str, current_user_id: str = Depends(get_current_user)):
    service = CommentService()
    deleted = service.delete_comment(comment_id, current_user_id)
    if deleted:
        return {"message": "Comment deleted successfully"}
    raise HTTPException(status_code=404, detail="Comment not found")
