from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schemas import *
from app.controllers.dependencies import *
from typing import List
from app.exceptions.exceptions import NotFoundError

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", response_model=RegularUserResponse, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(data.username, data.password)
    return user


@router.get("", status_code=200)
def display_all_users(service: UserService = Depends(get_user_service)):
    users = service.get_all_users()
    return MultipleUserResponse(count=len(users), users=users)


@router.get("/{user_id}", status_code=200)
def display_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        user_data = service.get_user(user_id)
        post_data = service.get_user_posts(user_id)
        return UserResponseWithPosts(
            username=user_data["username"],
            id=user_data["id"],
            created_at=user_data["created_at"],
            posts=post_data,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
