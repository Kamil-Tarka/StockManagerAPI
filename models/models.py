from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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
    roles: list[ReadRoleDto]


class CreateUserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)
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

    user_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)
