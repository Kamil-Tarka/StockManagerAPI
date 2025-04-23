from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt
from fastapi import HTTPException
from jose import JWTError
from starlette import status

from app_settings import AppSettings
from exceptions.exceptions import (
    InvalidCredentialsException,
    InvalidRoleException,
    TokenExpiredException,
    UserAccountIsDisabledException,
    WrongTokenTypeException,
    WrongUsernameException,
)
from models.entities import User
from models.models import LoginUserDto, RefreshTokenBody, TokenResponse
from services.role_service import RoleService
from services.user_service import UserService


class AuthService:
    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)
        self.role_service = RoleService(db)
        self.app_settings = AppSettings()

    def create_access_token(self, user: User):
        expires = datetime.now(ZoneInfo("Europe/Warsaw")) + timedelta(
            minutes=self.app_settings.token_expiration_time
        )
        to_encode = {
            "id": user.id,
            "sub": user.user_name,
            "role": {"id": user.role.id, "name": user.role.name},
            "exp": expires,
        }

        return jwt.encode(
            to_encode,
            self.app_settings.secret_key,
            algorithm=self.app_settings.token_algorithm,
        )

    def create_refresh_token(self, user: User):
        expires = datetime.now(ZoneInfo("Europe/Warsaw")) + timedelta(
            minutes=self.app_settings.refresh_token_expiration_time
        )
        to_encode = {
            "token_type": "refresh",
            "id": user.id,
            "sub": user.user_name,
            "role": {"id": user.role.id, "name": user.role.name},
            "exp": expires,
        }

        return jwt.encode(
            to_encode,
            self.app_settings.secret_key,
            algorithm=self.app_settings.token_algorithm,
        )

    def login_user(self, login_user_data: LoginUserDto) -> TokenResponse:
        user = self.user_service.verify_user_password(login_user_data)
        if user.is_active is False:
            raise UserAccountIsDisabledException(
                f"User with user_name={login_user_data.username} is disabled"
            )
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
        )

    def refresh_user_token(self, refresh_token: RefreshTokenBody) -> TokenResponse:
        try:
            payload = jwt.decode(
                refresh_token.refresh_token,
                self.app_settings.secret_key,
                algorithms=[self.app_settings.token_algorithm],
            )
            if payload.get("token_type") != "refresh":
                raise WrongTokenTypeException(f"Invalid token type")
            subject: str = payload.get("sub")
            user_id = payload.get("id")
            user = self.user_service.get_user_by_id(user_id)
            user_role = payload.get("role")
            role = self.role_service.get_role_by_id(user_role.get("id"))
            if role.name != user_role.get("name"):
                raise InvalidRoleException(f"Roles do not match")
            if user.is_active is False:
                raise UserAccountIsDisabledException(f"User is disabled")
            if user.user_name != subject:
                raise WrongUsernameException(f"Invalid username")
            access_token = self.create_access_token(user)
            new_refresh_token = self.create_refresh_token(user)
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                refresh_token=new_refresh_token,
            )
        except JWTError:
            raise InvalidCredentialsException(f"Invalid credentials")
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException(f"Token expired")

    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.app_settings.secret_key,
                algorithms=[self.app_settings.token_algorithm],
            )
            if payload.get("token_type") == "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                )
            subject: str = payload.get("sub")
            user_id = payload.get("id")
            user = self.user_service.get_user_by_id(user_id)
            user_role = payload.get("role")
            if user.is_active is False:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user",
                )
            if user.user_name != subject:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
            return {"id": user.id, "user_name": user.user_name, "role": user_role}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
