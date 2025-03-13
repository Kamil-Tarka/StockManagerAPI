from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.dependencies import get_auth_service
from models.models import LoginUserDto, Token
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

service_dependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: service_dependency,
):
    login_user_dto = LoginUserDto(
        username=form_data.username, password=form_data.password
    )
    access_token = service.create_access_token(login_user_dto)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
