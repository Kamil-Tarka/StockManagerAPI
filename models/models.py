from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from models.entities import ItemCategory, Role, StockItem, User


class ReadItemCategoryDto(BaseModel):
    """
    Data transfer object for reading item category information.

    Attributes:
        id (int): Unique identifier of the category.
        name (str): Name of the category.
        creation_date (datetime): Date the category was created.
        last_modification_date (datetime): Date the category was last modified.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creation_date: datetime
    last_modification_date: datetime


class ReadStockItemDto(BaseModel):
    """
    Data transfer object for reading stock item information.

    Attributes:
        id (int): Unique identifier of the stock item.
        name (str): Name of the stock item.
        description (Optional[str]): Description of the stock item.
        quantity (int): Quantity in stock.
        creation_date (datetime): Date the item was created.
        last_modification_date (datetime): Date the item was last modified.
        category (ReadItemCategoryDto): Category of the stock item.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    creation_date: datetime
    last_modification_date: datetime
    category: ReadItemCategoryDto


class CreateItemCategoryDto(BaseModel):
    """
    Data transfer object for creating a new item category.

    Attributes:
        name (str): Name of the new category.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)


class UpdateItemCategoryDto(BaseModel):
    """
    Data transfer object for updating an existing item category.

    Attributes:
        name (Optional[str]): New name for the category.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)


class CreateStockItemDto(BaseModel):
    """
    Data transfer object for creating a new stock item.

    Attributes:
        name (str): Name of the stock item.
        description (Optional[str]): Description of the stock item.
        quantity (int): Quantity in stock.
        category_id (int): ID of the category the item belongs to.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    quantity: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)


class UpdateStockItemDto(BaseModel):
    """
    Data transfer object for updating an existing stock item.

    Attributes:
        name (Optional[str]): New name for the stock item.
        description (Optional[str]): New description.
        quantity (Optional[int]): New quantity.
        category_id (Optional[int]): New category ID.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)
    description: Optional[str] = None
    quantity: int | None = Field(None, gt=0)
    category_id: int | None = Field(None, gt=0)


class ReadRoleDto(BaseModel):
    """
    Data transfer object for reading role information.

    Attributes:
        id (int): Unique identifier of the role.
        name (str): Name of the role.
        creation_date (datetime): Date the role was created.
        last_modification_date (datetime): Date the role was last modified.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creation_date: datetime
    last_modification_date: datetime


class CreateRoleDto(BaseModel):
    """
    Data transfer object for creating a new role.

    Attributes:
        name (str): Name of the new role.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)


class UpdateRoleDto(BaseModel):
    """
    Data transfer object for updating an existing role.

    Attributes:
        name (Optional[str]): New name for the role.
    """

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)


class ReadUserDto(BaseModel):
    """
    Data transfer object for reading user information.

    Attributes:
        id (int): Unique identifier of the user.
        user_name (str): Username of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        is_active (bool): Whether the user is active.
        creation_date (datetime): Date the user was created.
        last_modification_date (datetime): Date the user was last modified.
        role (ReadRoleDto): Role assigned to the user.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_name: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    creation_date: datetime
    last_modification_date: datetime
    role: ReadRoleDto


class CreateUserDto(BaseModel):
    """
    Data transfer object for creating a new user.

    Attributes:
        user_name (str): Username of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        password (str): Password for the user.
        role_id (int): ID of the role assigned to the user.
    """

    model_config = ConfigDict(from_attributes=True)

    user_name: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, exclude=True)
    role_id: int = Field(..., gt=0)


class UpdateUserDto(BaseModel):
    """
    Data transfer object for updating an existing user.

    Attributes:
        user_name (Optional[str]): New username.
        first_name (Optional[str]): New first name.
        last_name (Optional[str]): New last name.
        email (Optional[str]): New email address.
        password (Optional[str]): New password.
        is_active (Optional[bool]): New active status.
        role_id (Optional[int]): New role ID.
    """

    model_config = ConfigDict(from_attributes=True)

    user_name: str | None = Field(None, min_length=1, max_length=50)
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    email: str | None = Field(None, min_length=1, max_length=50)
    password: str | None = Field(None, min_length=8)
    is_active: bool | None = None
    role_id: int | None = Field(None, gt=0)


class LoginUserDto(BaseModel):
    """
    Data transfer object for user login credentials.

    Attributes:
        username (str): Username for login.
        password (str): Password for login.
    """

    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    """
    Data transfer object for authentication token response.

    Attributes:
        access_token (str): Access token.
        token_type (str): Type of the token.
        refresh_token (str): Refresh token.
    """

    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenBody(BaseModel):
    """
    Data transfer object for refresh token request body.

    Attributes:
        refresh_token (str): Refresh token.
    """

    refresh_token: str


T = TypeVar("T ")


class PagedResult(BaseModel, Generic[T]):
    """
    Generic data transfer object for paginated results.

    Attributes:
        data (List[T]): List of items on the current page.
        current_page (int): Current page number.
        page_size (int): Number of items per page.
        total_items (int): Total number of items.
        total_pages (int): Total number of pages.
    """

    model_config = ConfigDict(from_attributes=True)

    data: List[T]
    current_page: int
    page_size: int
    total_items: int
    total_pages: int


class SortDirection(str, Enum):
    """
    Enumeration for sort direction values.

    Values:
        asc: Ascending order.
        desc: Descending order.
    """

    asc = "asc"
    desc = "desc"


class BaseQuery(BaseModel):
    """
    Base class for query models supporting pagination and sorting.

    Attributes:
        page (int): The current page number (default: 1).
        page_size (int): The number of items per page (default: 10).
        sort_by (Optional[str]): Field to sort by.
        sort_direction (SortDirection): Sorting direction (asc or desc).
    """

    model_config = ConfigDict(from_attributes=True)

    page: int = Field(1, gt=0)
    page_size: int = Field(10, gt=0)
    sort_by: Optional[str] = Field(None, max_length=50)
    sort_direction: SortDirection = Field(SortDirection.asc)


class UserFilterQuery(BaseQuery):
    """
    Query model for filtering users with various criteria.

    Inherits pagination and sorting parameters from BaseQuery:
        page (int): The current page number (default: 1).
        page_size (int): The number of items per page (default: 10).
        sort_by (Optional[str]): Field to sort by.
        sort_direction (SortDirection): Sorting direction (asc or desc).

    Attributes:
        user_name (Optional[str]): Filter by user name.
        first_name (Optional[str]): Filter by first name.
        last_name (Optional[str]): Filter by last name.
        email (Optional[str]): Filter by email.
        is_active (Optional[bool]): Filter by active status.
        role_name (Optional[str]): Filter by role name.
    """

    model_config = ConfigDict(from_attributes=True)

    user_name: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    role_name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
        """
        Constructs a list of SQLAlchemy filter expressions based on the provided filter fields.
        Returns:
            list: List of filter expressions for querying users.
        """
        filter_list = []
        if self.user_name:
            filter_list.append(User.user_name.like(f"%{self.user_name}%"))
        if self.first_name:
            filter_list.append(User.first_name.like(f"%{self.first_name}%"))
        if self.last_name:
            filter_list.append(User.last_name.like(f"%{self.last_name}%"))
        if self.email:
            filter_list.append(User.email.like(f"%{self.email}%"))
        if self.is_active is not None:
            filter_list.append(User.is_active == self.is_active)
        if self.role_name:
            filter_list.append(User.role.has(Role.name.like(f"%{self.role_name}%")))
        return filter_list


class StockItemQuery(BaseQuery):
    """
    Query model for filtering stock items with various criteria.

    Inherits pagination and sorting parameters from BaseQuery:
        page (int): The current page number (default: 1).
        page_size (int): The number of items per page (default: 10).
        sort_by (Optional[str]): Field to sort by.
        sort_direction (SortDirection): Sorting direction (asc or desc).

    Attributes:
        name (Optional[str]): Filter by item name.
        description (Optional[str]): Filter by description.
        quantity (Optional[int]): Filter by quantity.
        category_name (Optional[str]): Filter by category name.
    """

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = None
    category_name: Optional[str] = Field(None, max_length=50)

    @field_validator("quantity", mode="before")
    def validate_quantity(cls, value):
        if value is None or value == "":
            return None
        try:
            quantity = int(value)
            if quantity >= 0:
                return quantity
            raise ValueError("Quantity must be a non-negative integer.")
        except ValueError:
            raise ValueError("Quantity must be a valid non-negative integer.")

    @property
    def filter_list(self):
        filter_list = []
        if self.name:
            filter_list.append(StockItem.name.like(f"%{self.name}%"))
        if self.description:
            filter_list.append(StockItem.description.like(f"%{self.description}%"))
        if self.quantity is not None:
            filter_list.append(StockItem.quantity == self.quantity)
        if self.category_name:
            filter_list.append(
                StockItem.category.has(
                    ItemCategory.name.like(f"%{self.category_name}%")
                )
            )
        return filter_list


class RoleFilterQuery(BaseQuery):
    """
    Query model for filtering roles by name.

    Inherits pagination and sorting parameters from BaseQuery:
        page (int): The current page number (default: 1).
        page_size (int): The number of items per page (default: 10).
        sort_by (Optional[str]): Field to sort by.
        sort_direction (SortDirection): Sorting direction (asc or desc).

    Attributes:
        name (Optional[str]): Filter by role name.
    """

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
        filter_list = []
        if self.name:
            filter_list.append(Role.name.like(f"%{self.name}%"))
        return filter_list


class ItemCategoryFilterQuery(BaseQuery):
    """
    Query model for filtering item categories by name.

    Inherits pagination and sorting parameters from BaseQuery:
        page (int): The current page number (default: 1).
        page_size (int): The number of items per page (default: 10).
        sort_by (Optional[str]): Field to sort by.
        sort_direction (SortDirection): Sorting direction (asc or desc).

    Attributes:
        name (Optional[str]): Filter by category name.
    """

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
        filter_list = []
        if self.name:
            filter_list.append(ItemCategory.name.like(f"%{self.name}%"))
        return filter_list
