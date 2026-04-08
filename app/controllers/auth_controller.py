from fastapi import APIRouter, Depends, HTTPException
from app.controllers.dependencies import get_user_service
from app.security.auth import create_access_token
from app.schemas.schemas import *

router = APIRouter(
  prefix="/auth",
  tags=["auth"],
)

@router.post("auth/login", response_model=TokenResponse)
def login(data: LoginRequest, service = Depends(get_user_service)):
    validate = service.verify_credentials(data.username, data.password)
    if validate == 1:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    elif validate == 2:
        raise HTTPException(
            status_code=404,
            detail="Wrong password"
        )
    else:
        token = create_access_token(validate[0]["id"])
        return {
            "access_token": token,
            "token_type": "bearer"
        }