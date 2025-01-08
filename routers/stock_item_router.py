from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from database_settings import get_db_session
from services.services import StockItemService, get_stock_item_service

router = APIRouter(prefix="/stock-items", tags=["stock-items"])
db_session = Annotated[Session, Depends(get_db_session)]
service_dependency = Annotated[
    StockItemService,
    Depends(get_stock_item_service),
]


@router.get(
    "/{stock_item_id}",
    status_code=status.HTTP_200_OK,
)
async def read_stock_item(
    db: db_session, service: service_dependency, stock_item_id: int = Path(gt=0)
):
    stock_item_model = service.get_stock_item(db, stock_item_id)
    if stock_item_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock item with id={stock_item_id} not found",
        )
    return stock_item_model
