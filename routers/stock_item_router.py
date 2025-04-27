from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from dependencies.dependencies import get_current_user, get_stock_item_service
from exceptions.exceptions import (
    CategoryNotFoundException,
    StockItemAlreadyExistsException,
    StockItemNotFoundException,
)
from models.models import (
    CreateStockItemDto,
    PagedResult,
    ReadStockItemDto,
    StockItemQuery,
    UpdateStockItemDto,
)
from services.stock_item_service import StockItemService

router = APIRouter(prefix="/stock-items", tags=["stock-items"])

service_dependency = Annotated[StockItemService, Depends(get_stock_item_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/{stock_item_id}", response_model=ReadStockItemDto, status_code=status.HTTP_200_OK
)
async def read_stock_item(
    user: user_dependency, service: service_dependency, stock_item_id: int = Path(gt=0)
):
    """
    Return a stock item by ID.
    Args:
        user: Current user dependency.
        service: Stock item service dependency.
        stock_item_id (int): ID of the stock item to return.
    Returns:
        ReadStockItemDto: Stock item data.
    Raises:
        HTTPException: If stock item is not found.
    """
    try:
        stock_item_model = service.get_stock_item_by_id(stock_item_id)
    except StockItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return stock_item_model


@router.get(
    "", response_model=PagedResult[ReadStockItemDto], status_code=status.HTTP_200_OK
)
async def read_all_stock_items(
    filter_query: Annotated[StockItemQuery, Query()],
    user: user_dependency,
    service: service_dependency,
):
    """
    Return a paginated list of stock items with optional filtering.
    Args:
        filter_query (StockItemQuery): Filtering and pagination options.
        user: Current user dependency.
        service: Stock item service dependency.
    Returns:
        PagedResult[ReadStockItemDto]: Paginated stock item data.
    """
    stock_items = service.get_all_stock_items(filter_query)
    return stock_items


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_stock_item(
    user: user_dependency,
    service: service_dependency,
    create_stock_item_dto: CreateStockItemDto,
):
    """
    Create a new stock item.
    Args:
        user: Current user dependency.
        service: Stock item service dependency.
        create_stock_item_dto (CreateStockItemDto): Data for the new stock item.
    Returns:
        str: Location of the created stock item resource.
    Raises:
        HTTPException: If stock item already exists or category not found.
    """
    try:
        created_stock_item = service.create_stock_item(create_stock_item_dto)
    except StockItemAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"api/v1/stock-items/{created_stock_item.id}"


@router.put("/{stock_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_stock_item(
    user: user_dependency,
    service: service_dependency,
    update_stock_item: UpdateStockItemDto,
    stock_item_id: int = Path(gt=0),
):
    """
    Update an existing stock item.
    Args:
        user: Current user dependency.
        service: Stock item service dependency.
        update_stock_item (UpdateStockItemDto): Data to update.
        stock_item_id (int): ID of the stock item to update.
    Returns:
        str: Update confirmation message.
    Raises:
        HTTPException: If stock item not found, category not found, or stock item already exists.
    """
    try:
        service.update_stock_item(stock_item_id, update_stock_item)
    except StockItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StockItemAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"StockItem with id={stock_item_id} updated."


@router.delete("/{stock_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_item(
    user: user_dependency, service: service_dependency, stock_item_id: int = Path(gt=0)
):
    """
    Delete a stock item by ID.
    Args:
        user: Current user dependency.
        service: Stock item service dependency.
        stock_item_id (int): ID of the stock item to delete.
    Returns:
        str: Deletion confirmation message.
    Raises:
        HTTPException: If stock item not found.
    """
    try:
        service.delete_stock_item(stock_item_id)
    except StockItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"StockItem with id={stock_item_id} deleted."
