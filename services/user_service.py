from datetime import datetime
from zoneinfo import ZoneInfo

from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.exceptions import (
    UserAccountIsDisabledException,
    UserAlreadyExistsException,
    UserNotFoundException,
    WrongPasswordException,
)
from models.entities import Role, User
from models.models import (
    CreateUserDto,
    LoginUserDto,
    PagedResult,
    UpdateUserDto,
    UserFilterQuery,
)
from paginate.paginate import paginate
from services.role_service import RoleService

"""
Service for managing user-related operations, including CRUD, authentication, and filtering.
"""


class UserService:
    """
    Provides user management operations such as create, read, update, delete, and authentication.
    """

    def __init__(self, db: Session):
        """
        Initialize UserService with a database session.
        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.role_service = RoleService(db)

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Return a user by their unique ID.
        Args:
            user_id (int): The user's ID.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If user is not found.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFoundException(f"User with id={user_id} not found")
        return user

    def get_all_users(self, filter_query: UserFilterQuery) -> PagedResult:
        """
        Return all users matching the filter query, with pagination and sorting.
        Args:
            filter_query (UserFilterQuery): Filtering and pagination options.
        Returns:
            PagedResult: Paginated result of users.
        """
        query = self.db.query(User).filter(and_(*filter_query.filter_list))
        total_count = query.count()

        if filter_query.sort_by == "role":
            query = query.join(Role)
            if filter_query.sort_direction == "asc":
                query = query.order_by(Role.name.asc())
            else:
                query = query.order_by(Role.name.desc())
        elif filter_query.sort_by is not None and hasattr(User, filter_query.sort_by):
            column = getattr(User, filter_query.sort_by)
            if filter_query.sort_direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())
        users = (
            query.offset((filter_query.page - 1) * filter_query.page_size)
            .limit(filter_query.page_size)
            .all()
        )
        paged_result = paginate(
            users, filter_query.page, filter_query.page_size, total_count
        )
        return paged_result

    def get_user_by_user_name(self, user_name: str) -> User | None:
        """
        Return a user by their username.
        Args:
            user_name (str): The user's username.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If user is not found.
        """
        user = self.db.query(User).filter(User.user_name == user_name).first()
        if user is None:
            raise UserNotFoundException(f"User with user_name={user_name} not found")
        return user

    def get_user_by_email(self, email: str) -> User | None:
        """
        Return a user by their email address.
        Args:
            email (str): The user's email.
        Returns:
            User: The user object if found.
        Raises:
            UserNotFoundException: If user is not found.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise UserNotFoundException(f"User with email={email} not found")
        return user

    def create_user(self, create_user_dto: CreateUserDto) -> User:
        """
        Create a new user in the database.
        Args:
            create_user_dto (CreateUserDto): Data for the new user.
        Returns:
            User: The created user object.
        Raises:
            UserAlreadyExistsException: If user with username or email already exists.
        """
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
                current_date = datetime.now(ZoneInfo("Europe/Warsaw"))
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
        """
        Update an existing user's information.
        Args:
            user_id (int): The user's ID.
            update_user_dto (UpdateUserDto): Data to update.
        Returns:
            User: The updated user object.
        Raises:
            UserAlreadyExistsException: If username or email already exists.
        """
        user = self.get_user_by_id(user_id)
        current_date = datetime.now(ZoneInfo("Europe/Warsaw"))

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
        """
        Delete a user by their ID.
        Args:
            user_id (int): The user's ID.
        Returns:
            User: The deleted user object.
        """
        user = self.get_user_by_id(user_id)

        self.db.delete(user)
        self.db.commit()
        return user

    def verify_user_password(self, login_data: LoginUserDto) -> User:
        """
        Verify a user's password for authentication.
        Args:
            login_data (LoginUserDto): Login credentials.
        Returns:
            User: The authenticated user object.
        Raises:
            UserAccountIsDisabledException: If user is disabled.
            WrongPasswordException: If password is incorrect.
        """
        user = self.get_user_by_user_name(login_data.username)
        if user.is_active is False:
            raise UserAccountIsDisabledException(
                f"User with user_name={login_data.username} is disabled"
            )
        if not self.bcrypt_context.verify(login_data.password, user.hashed_password):
            raise WrongPasswordException("Wrong password")
        return user

    def check_if_table_is_empty(self) -> bool:
        """
        Check if the user table is empty.
        Returns:
            bool: True if empty, False otherwise.
        """
        query = self.db.query(User)
        if query.count() == 0:
            return True
        return False
