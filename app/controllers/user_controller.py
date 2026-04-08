from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import *
from dependencies import *
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", response_model=UserResponse)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(data.username, data.password)
    return user


@router.get("", response_model=List[UserResponse])
def display_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def display_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
