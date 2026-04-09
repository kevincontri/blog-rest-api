from fastapi import APIRouter, Depends
from dependencies import *
from app.security.auth import get_current_user
from app.schemas.post_schemas import *
from app.services.post_services import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/posts", response_model=PostCreateResponse)
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
