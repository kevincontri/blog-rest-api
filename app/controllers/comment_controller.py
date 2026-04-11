from fastapi import APIRouter, Depends, HTTPException
from dependencies import *
from app.schemas.comment_schemas import *
from app.services.comment_services import CommentService
from typing import List
from exceptions.exceptions import NotFoundError
from app.security.auth import get_current_user
from app.server.server import app

router = APIRouter(prefix="/comments", tags=["comments"])

service = CommentService()


@app.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user_id: int = Depends(get_current_user),
):
    return service.create_comment(post_id, current_user_id, comment.content)


@app.get(
    "/posts/{post_id}/comments", response_model=List[CommentResponse], status_code=200
)
def get_comments_from_post(post_id: int):
    try:
        comments = service.get_comments_from_post(post_id)
        return comments if comments else []
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{comment_id}", response_model=CommentResponse, status_code=200)
def get_comment(comment_id: int):
    try:
        return service.get_comment(comment_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, current_user_id: int = Depends(get_current_user)):
    try:
        deleted = service.delete_comment(comment_id, current_user_id)
        if deleted:
            return
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
