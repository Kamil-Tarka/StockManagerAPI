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

"""
Service for authentication, token management, and user session validation.
"""


class AuthService:
    """
    Provides authentication operations, including login, token creation, refresh, and user validation.
    """

    def __init__(self, db):
        """
        Initialize AuthService with a database session.
        Args:
            db: SQLAlchemy session object.
        """
        self.db = db
        self.user_service = UserService(db)
        self.role_service = RoleService(db)
        self.app_settings = AppSettings()

    def create_access_token(self, user: User):
        """
        Create a JWT access token for a user.
        Args:
            user (User): The user object.
        Returns:
            str: Encoded JWT access token.
        """
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
        """
        Create a JWT refresh token for a user.
        Args:
            user (User): The user object.
        Returns:
            str: Encoded JWT refresh token.
        """
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
        """
        Authenticate a user and return access and refresh tokens.
        Args:
            login_user_data (LoginUserDto): Login credentials.
        Returns:
            TokenResponse: Access and refresh tokens.
        Raises:
            UserAccountIsDisabledException: If user is disabled.
        """
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
        """
        Refresh a user's access and refresh tokens using a valid refresh token.
        Args:
            refresh_token (RefreshTokenBody): The refresh token data.
        Returns:
            TokenResponse: New access and refresh tokens.
        Raises:
            WrongTokenTypeException: If token type is invalid.
            InvalidRoleException: If user role does not match.
            UserAccountIsDisabledException: If user is disabled.
            WrongUsernameException: If username does not match.
            InvalidCredentialsException: If credentials are invalid.
            TokenExpiredException: If token is expired.
        """
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
        """
        Validate and return the current user from a JWT access token.
        Args:
            token (str): JWT access token.
        Returns:
            dict: User information (id, user_name, role).
        Raises:
            HTTPException: If token is invalid, expired, or user is inactive.
        """
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
