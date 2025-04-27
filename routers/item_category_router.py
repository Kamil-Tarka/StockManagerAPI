from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from dependencies.dependencies import get_current_user, get_item_category_service
from exceptions.exceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
)
from models.models import (
    CreateItemCategoryDto,
    ItemCategoryFilterQuery,
    PagedResult,
    ReadItemCategoryDto,
    UpdateItemCategoryDto,
)
from services.item_category_service import ItemCategoryService

router = APIRouter(prefix="/item-categories", tags=["item-categories"])

service_dependency = Annotated[ItemCategoryService, Depends(get_item_category_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{item_category_id}", response_model=ReadItemCategoryDto, status_code=200)
async def read_item_category(
    user: user_dependency,
    service: service_dependency,
    item_category_id: int = Path(gt=0),
):
    """
    Return an item category by ID.
    Args:
        user: Current user dependency.
        service: Item category service dependency.
        item_category_id (int): ID of the item category to return.
    Returns:
        ReadItemCategoryDto: Item category data.
    Raises:
        HTTPException: If item category is not found.
    """
    try:
        item_category = service.get_item_category_by_id(item_category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return item_category


@router.get("", response_model=PagedResult[ReadItemCategoryDto], status_code=200)
async def read_all_item_categories(
    filter_query: Annotated[ItemCategoryFilterQuery, Query()],
    user: user_dependency,
    service: service_dependency,
):
    """
    Return a paginated list of item categories with optional filtering.
    Args:
        filter_query (ItemCategoryFilterQuery): Filtering and pagination options.
        user: Current user dependency.
        service: Item category service dependency.
    Returns:
        PagedResult[ReadItemCategoryDto]: Paginated item category data.
    """
    item_categories = service.get_all_item_categories(filter_query)
    return item_categories


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item_category(
    user: user_dependency,
    service: service_dependency,
    create_item_category_dto: CreateItemCategoryDto,
):
    """
    Create a new item category.
    Args:
        user: Current user dependency.
        service: Item category service dependency.
        create_item_category_dto (CreateItemCategoryDto): Data for the new item category.
    Returns:
        str: Location of the created item category resource.
    Raises:
        HTTPException: If item category already exists.
    """
    try:
        created_item_category = service.create_item_category(create_item_category_dto)
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"api/v1/item-categories/{created_item_category.id}"


@router.put("/{item_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item_category(
    user: user_dependency,
    service: service_dependency,
    item_category: UpdateItemCategoryDto,
    item_category_id: int = Path(gt=0),
):
    """
    Update an existing item category.
    Args:
        user: Current user dependency.
        service: Item category service dependency.
        item_category (UpdateItemCategoryDto): Data to update.
        item_category_id (int): ID of the item category to update.
    Returns:
        str: Update confirmation message.
    Raises:
        HTTPException: If item category not found or already exists.
    """
    try:
        service.update_category(item_category_id, item_category)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"Item category with id={item_category_id} updated."


@router.delete("/{item_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_category(
    user: user_dependency,
    service: service_dependency,
    item_category_id: int = Path(gt=0),
):
    """
    Delete an item category by ID.
    Args:
        user: Current user dependency.
        service: Item category service dependency.
        item_category_id (int): ID of the item category to delete.
    Returns:
        str: Deletion confirmation message.
    Raises:
        HTTPException: If item category not found.
    """
    try:
        service.delete_category(item_category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"Item category with id={item_category_id} deleted."
