from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from dependencies.dependencies import get_current_user, get_stock_item_service
from models.models import CreateStockItemDto, ReadStockItemDto, UpdateStockItemDto
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
    stock_item_model = service.get_stock_item_by_id(stock_item_id)
    if stock_item_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock item with id={stock_item_id} not found",
        )
    return stock_item_model


@router.get("", response_model=list[ReadStockItemDto], status_code=status.HTTP_200_OK)
async def read_all_stock_items(user: user_dependency, service: service_dependency):
    stock_items = service.get_all_stock_items()
    return stock_items


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_stock_item(
    user: user_dependency,
    service: service_dependency,
    create_stock_item_dto: CreateStockItemDto,
):
    created_stock_item = service.create_stock_item(create_stock_item_dto)
    return f"api/v1/stock-items/{created_stock_item.id}"


@router.put("/{stock_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_stock_item(
    user: user_dependency,
    service: service_dependency,
    update_stock_item: UpdateStockItemDto,
    stock_item_id: int = Path(gt=0),
):
    service.update_stock_item(stock_item_id, update_stock_item)
    return f"StockItem with id={stock_item_id} updated."


@router.delete("/{stock_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_item(
    user: user_dependency, service: service_dependency, stock_item_id: int = Path(gt=0)
):
    service.delete_stock_item(stock_item_id)
    return f"StockItem with id={stock_item_id} deleted."
