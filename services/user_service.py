from datetime import datetime, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.entities import User
from models.models import CreateUserDto, LoginUserDto, UpdateUserDto
from services.roles_service import RolesService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.roles_service = RolesService(db)

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def get_all_users(self) -> list[User]:
        users = self.db.query(User).all()
        return users

    def get_user_by_user_name(self, user_name: str) -> User | None:
        user = self.db.query(User).filter(User.user_name == user_name).first()
        return user

    def create_user(self, create_user_dto: CreateUserDto) -> User:
        user = self.get_user_by_user_name(self.db, create_user_dto.user_name)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with user_name={create_user_dto.user_name} already exists",
            )
        if self.roles_service.get_role_by_id(create_user_dto.role_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id={create_user_dto.role_id} not found",
            )
        user = User(**create_user_dto.model_dump())
        user.hashed_password = self.bcrypt_context.hash(create_user_dto.password)
        current_date = datetime.now(timezone.utc)
        user.creation_date = current_date
        user.last_modification_date = current_date
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, update_user_dto: UpdateUserDto) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        if (
            update_user_dto.role_id
            and self.roles_service.get_role_by_id(update_user_dto.role_id) is None
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id={update_user_dto.role_id} not found",
            )
        current_date = datetime.now(timezone.utc)
        if update_user_dto.user_name and user.user_name != update_user_dto.user_name:
            user.user_name = update_user_dto.user_name
            user.last_modification_date = current_date
        if update_user_dto.first_name and user.first_name != update_user_dto.first_name:
            user.first_name = update_user_dto.first_name
            user.last_modification_date = current_date
        if update_user_dto.last_name and user.last_name != update_user_dto.last_name:
            user.last_name = update_user_dto.last_name
            user.last_modification_date = current_date
        if update_user_dto.email and user.email != update_user_dto.email:
            user.email = update_user_dto.email
            user.last_modification_date = current_date
        if update_user_dto.password:
            user.password = self.bcrypt_context.hash(update_user_dto.password)
            user.last_modification_date = current_date
        if (
            update_user_dto.is_active is not None
            and user.is_active != update_user_dto.is_active
        ):
            user.is_active = update_user_dto.is_active
            user.last_modification_date = current_date
        if update_user_dto.role_id and user.role_id != update_user_dto.role_id:
            if self.roles_service.get_role_by_id(update_user_dto.role_id) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id={update_user_dto.role_id} not found",
                )
            user.role_id = update_user_dto.role_id
            user.last_modification_date = current_date
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        self.db.delete(user)
        self.db.commit()
        return user

    def verify_user_password(self, login_data: LoginUserDto) -> User:
        user = self.get_user_by_user_name(login_data.user_name)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_name={login_data.user_name} not found",
            )
        if not self.bcrypt_context.verify(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )
        return user
