from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schemas import *
from app.controllers.dependencies import *
from typing import List
from app.exceptions.exceptions import NotFoundError

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(data.username, data.password)
    return user


@router.get("", response_model=List[UserResponse], status_code=200)
def display_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def display_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        return service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
