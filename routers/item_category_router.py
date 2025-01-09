from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database_settings import get_db_session
from models.models import (
    CreateItemCategoryDto,
    ReadItemCategoryDto,
    UpdateItemCategoryDto,
)
from services.item_category_service import (
    ItemCategoryService,
    get_item_category_service,
)

router = APIRouter(prefix="/item-categories", tags=["item-categories"])

db_session = Annotated[Session, Depends(get_db_session)]
service_dependency = Annotated[
    ItemCategoryService,
    Depends(get_item_category_service),
]


@router.get("/{item_category_id}", response_model=ReadItemCategoryDto, status_code=200)
async def read_item_category(
    db: db_session, service: service_dependency, item_category_id: int
):
    item_category = service.get_item_category_by_id(db, item_category_id)
    if item_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item category with id={item_category_id} not found",
        )
    return item_category


@router.get("", response_model=list[ReadItemCategoryDto], status_code=200)
async def read_all_item_categories(db: db_session, service: service_dependency):
    item_categories = service.get_all_item_categories(db)
    return item_categories


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item_category(
    db: db_session,
    service: service_dependency,
    create_item_category_dto: CreateItemCategoryDto,
):
    created_item_category = service.create_item_category(db, create_item_category_dto)
    return f"api/v1/item-categories{created_item_category.id}"


@router.put("/{item_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item_category(
    db: db_session,
    service: service_dependency,
    item_category: UpdateItemCategoryDto,
    item_category_id: int,
):
    service.update_item_category(db, item_category_id, item_category)


@router.delete("/{item_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_category(
    db: db_session, service: service_dependency, item_category_id: int
):
    service.delete_item_category(db, item_category_id)
