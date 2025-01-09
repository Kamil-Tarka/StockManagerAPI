from datetime import datetime
from typing import List, Optional

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
    amount: int
    creation_date: datetime
    last_modification_date: datetime
    categories: List[ReadItemCategoryDto]


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
    amount: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)


class UpdateStockItemDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=50)
    description: Optional[str] = None
    amount: int | None = Field(None, gt=0)
    category_id: int | None = Field(None, gt=0)
