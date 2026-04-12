from fastapi import APIRouter, Depends, HTTPException
from app.controllers.dependencies import *
from app.security.auth import get_current_user
from app.schemas.post_schemas import *
from app.services.post_services import PostService
from typing import List
from app.exceptions.exceptions import NotFoundError

router = APIRouter(prefix="/posts", tags=["posts"])

service = PostService()


@router.post("", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, current_user_id: int = Depends(get_current_user)):
    post = service.create_post(post.title, post.content, current_user_id)
    return post


@router.get("", status_code=200)
def get_posts(
    author_id: int | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    try:
        posts = service.get_post_query(author_id, search, sort_by, page, limit)
        return MultiplePostFormat(count=len(posts), posts=posts)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{post_id}", status_code=200)
def display_post(post_id: int):
    try:
        post_data = service.get_post(post_id)
        comments_data = service.get_comments_from_post(post_id)
        return PostWithCommentsResponse(post=post_data, post_comments=comments_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{post_id}", response_model=PostResponse, status_code=200)
def update_post(
    post_id: int, post: PostUpdate, current_user_id: int = Depends(get_current_user)
):
    if post.title is None and post.content is None:
        raise HTTPException(status_code=400, detail="Bad Request Body")
    try:
        return service.update_post(post_id, current_user_id, post.title, post.content)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, current_user_id: int = Depends(get_current_user)):
    try:
        post_deleted = service.delete_post(post_id, current_user_id)
        if post_deleted:
            return
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
