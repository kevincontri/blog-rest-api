from fastapi import APIRouter, Depends, HTTPException
from app.controllers.dependencies import get_user_service
from app.security.auth import create_access_token
from app.schemas.auth_schemas import *
from app.exceptions.exceptions import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service=Depends(get_user_service)):
    try:
        validate = service.verify_credentials(data.username, data.password)
    except WrongCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    token = create_access_token(validate["id"])
    return {"access_token": token, "token_type": "bearer"}
