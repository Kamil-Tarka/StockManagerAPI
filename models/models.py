from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


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
    price: float
    quantity: int
    amount: float
    creation_date: datetime
    last_modification_date: datetime
    categories: List[ReadItemCategoryDto]
