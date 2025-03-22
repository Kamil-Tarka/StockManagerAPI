from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.dependencies import get_auth_service
from exceptions.exceptions import (
    InvalidCredentialsException,
    InvalidRoleException,
    TokenExpiredException,
    UserAccountIsDisabledException,
    UserNotFoundException,
    WrongPasswordException,
    WrongTokenTypeException,
    WrongUsernameException,
)
from models.models import LoginUserDto, RefreshTokenBody, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

service_dependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: service_dependency,
):
    try:
        login_user_dto = LoginUserDto(
            username=form_data.username, password=form_data.password
        )
        access_token = service.login_user(login_user_dto)

    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAccountIsDisabledException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return access_token


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(service: service_dependency, refresh_token: RefreshTokenBody):
    try:
        new_token = service.refresh_user_token(refresh_token)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAccountIsDisabledException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WrongTokenTypeException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InvalidRoleException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WrongUsernameException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WrongTokenTypeException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except TokenExpiredException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return new_token
