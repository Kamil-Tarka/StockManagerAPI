from datetime import datetime, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.entities import User
from models.models import CreateUserDto, UpdateUserDto
from services.roles_service import RolesService


class UserService:

    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        user = db.query(User).filter(User.id == user_id).first()
        return user

    def get_all_users(self, db: Session) -> list[User]:
        users = db.query(User).all()
        return users

    def get_user_by_user_name(self, db: Session, user_name: str) -> User | None:
        user = db.query(User).filter(User.user_name == user_name).first()
        return user

    def create_user(self, db: Session, create_user_dto: CreateUserDto) -> User:
        user = self.get_user_by_user_name(db, create_user_dto.user_name)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with user_name={create_user_dto.user_name} already exists",
            )
        if RolesService.get_role_by_id(db, create_user_dto.role_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id={create_user_dto.role_id} not found",
            )
        user = User(**create_user_dto.model_dump())
        user.hashed_password = self.bcrypt_context.hash(create_user_dto.password)
        current_date = datetime.now(timezone.utc)
        user.creation_date = current_date
        user.last_modification_date = current_date
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_user(
        self, db: Session, user_id: int, update_user_dto: UpdateUserDto
    ) -> User:
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        if (
            update_user_dto.role_id
            and RolesService.get_role_by_id(db, update_user_dto.role_id) is None
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
            if RolesService.get_role_by_id(db, update_user_dto.role_id) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id={update_user_dto.role_id} not found",
                )
            user.role_id = update_user_dto.role_id
            user.last_modification_date = current_date
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int) -> User:
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        db.delete(user)
        db.commit()
        return user

    def authenticate_user(self, db: Session, user_name: str, password: str) -> User:
        user = self.get_user_by_user_name(db, user_name)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with user_name={user_name} not found",
            )
        if not self.bcrypt_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )
        return user


def get_user_service() -> UserService:
    return UserService()
