from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from models.entities import ItemCategory, Role, StockItem, User


class ReadItemCategoryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creation_date: datetime
    last_modification_date: datetime


class ReadStockItemDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    creation_date: datetime
    last_modification_date: datetime
    category: ReadItemCategoryDto


class CreateItemCategoryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)


class UpdateItemCategoryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)


class CreateStockItemDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    quantity: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)


class UpdateStockItemDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)
    description: Optional[str] = None
    quantity: int | None = Field(None, gt=0)
    category_id: int | None = Field(None, gt=0)


class ReadRoleDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creation_date: datetime
    last_modification_date: datetime


class CreateRoleDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=50)


class UpdateRoleDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)


class ReadUserDto(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)

    user_name: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, exclude=True)
    role_id: int = Field(..., gt=0)


class UpdateUserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str | None = Field(None, min_length=1, max_length=50)
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    email: str | None = Field(None, min_length=1, max_length=50)
    password: str | None = Field(None, min_length=8)
    is_active: bool | None = None
    role_id: int | None = Field(None, gt=0)


class LoginUserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenBody(BaseModel):
    refresh_token: str


T = TypeVar("T ")


class PagedResult(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    data: List[T]
    current_page: int
    page_size: int
    total_items: int
    total_pages: int


class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class BaseQuery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    page: int = Field(1, gt=0)
    page_size: int = Field(10, gt=0)
    sort_by: Optional[str] = Field(None, max_length=50)
    sort_direction: SortDirection = Field(SortDirection.asc)


class UserFilterQuery(BaseQuery):
    model_config = ConfigDict(from_attributes=True)

    user_name: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    role_name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
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
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
        filter_list = []
        if self.name:
            filter_list.append(Role.name.like(f"%{self.name}%"))
        return filter_list


class ItemCategoryFilterQuery(BaseQuery):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, max_length=50)

    @property
    def filter_list(self):
        filter_list = []
        if self.name:
            filter_list.append(ItemCategory.name.like(f"%{self.name}%"))
        return filter_list
