from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from exceptions.exceptions import (
    UserAccountIsDisabledException,
    UserAlreadyExistsException,
    UserNotFoundException,
    WrongPasswordException,
)
from models.entities import User
from models.models import CreateUserDto, LoginUserDto, UpdateUserDto
from services.role_service import RoleService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.role_service = RoleService(db)

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFoundException(f"User with id={user_id} not found")
        return user

    def get_all_users(self) -> list[User]:
        users = self.db.query(User).all()
        return users

    def get_user_by_user_name(self, user_name: str) -> User | None:
        user = self.db.query(User).filter(User.user_name == user_name).first()
        if user is None:
            raise UserNotFoundException(f"User with user_name={user_name} not found")
        return user

    def get_user_by_email(self, email: str) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise UserNotFoundException(f"User with email={email} not found")
        return user

    def create_user(self, create_user_dto: CreateUserDto) -> User:
        try:
            user = self.get_user_by_user_name(create_user_dto.user_name)
        except UserNotFoundException:
            try:
                self.get_user_by_email(create_user_dto.email)
            except UserNotFoundException:
                self.role_service.get_role_by_id(create_user_dto.role_id)

                user = User(**create_user_dto.model_dump())
                user.hashed_password = self.bcrypt_context.hash(
                    create_user_dto.password
                )
                current_date = datetime.now(timezone.utc)
                user.creation_date = current_date
                user.last_modification_date = current_date
                user.is_active = True
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                return user
            else:
                raise UserAlreadyExistsException(
                    f"User with email={create_user_dto.email} already exists"
                )
        else:
            raise UserAlreadyExistsException(
                f"User with user_name={user.user_name} already exists"
            )

    def update_user(self, user_id: int, update_user_dto: UpdateUserDto) -> User:
        user = self.get_user_by_id(user_id)
        current_date = datetime.now(timezone.utc)

        if update_user_dto.user_name and user.user_name != update_user_dto.user_name:
            try:
                self.get_user_by_user_name(update_user_dto.user_name)
            except UserNotFoundException:
                user.user_name = update_user_dto.user_name
                user.last_modification_date = current_date
            else:
                raise UserAlreadyExistsException(
                    f"User with user_name={update_user_dto.user_name} already exists"
                )
        if update_user_dto.first_name and user.first_name != update_user_dto.first_name:
            user.first_name = update_user_dto.first_name
            user.last_modification_date = current_date
        if update_user_dto.last_name and user.last_name != update_user_dto.last_name:
            user.last_name = update_user_dto.last_name
            user.last_modification_date = current_date
        if update_user_dto.email and user.email != update_user_dto.email:
            try:
                self.get_user_by_email(update_user_dto.email)
            except UserNotFoundException:
                user.email = update_user_dto.email
                user.last_modification_date = current_date
            else:
                raise UserAlreadyExistsException(
                    f"User with email={update_user_dto.email} already exists"
                )
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
            self.role_service.get_role_by_id(update_user_dto.role_id)

            user.role_id = update_user_dto.role_id
            user.last_modification_date = current_date
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> User:
        user = self.get_user_by_id(user_id)

        self.db.delete(user)
        self.db.commit()
        return user

    def verify_user_password(self, login_data: LoginUserDto) -> User:
        user = self.get_user_by_user_name(login_data.username)
        if user.is_active is False:
            raise UserAccountIsDisabledException(
                f"User with user_name={login_data.username} is disabled"
            )
        if not self.bcrypt_context.verify(login_data.password, user.hashed_password):
            raise WrongPasswordException("Wrong password")
        return user
