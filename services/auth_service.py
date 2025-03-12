from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from app_settings import AppSettings
from models.models import LoginUserDto
from services.user_service import UserService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthService:
    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)
        self.app_settings = AppSettings()

    def create_access_token(self, login_user_data: LoginUserDto):
        user = self.user_service.verify_user_password(login_user_data)
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=self.app_settings.token_expiration_time
        )
        encode = {
            "id": user.id,
            "sub": user.user_name,
            "role": {"id": user.role.id, "name": user.role.name},
            "exp": expires,
        }

        return jwt.encode(
            encode, self.app_settings.secret_key, self.app_settings.token_algorithm
        )

    def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(
                token,
                self.app_settings.secret_key,
                algorithms=[self.app_settings.token_algorithm],
            )
            subject: str = payload.get("sub")
            user_id = payload.get("id")
            user = self.user_service.get_user_by_id(user_id)
            user_role = payload.get("role")
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
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
