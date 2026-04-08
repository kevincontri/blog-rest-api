from fastapi import APIRouter, Depends
from app.services import UserService
from app.schemas import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("", response_model=UserResponse)
def create_user(data: UserCreate, service: UserService = Depends()):
    