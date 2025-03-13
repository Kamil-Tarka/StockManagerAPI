from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.entities import StockItem
from models.models import CreateStockItemDto, UpdateStockItemDto
from services.item_category_service import ItemCategoryService


class StockItemService:
    def __init__(self, db: Session):
        self.db = db
        self.item_category_service = ItemCategoryService(db)

    def get_stock_item_by_id(self, stock_item_id: int) -> StockItem | None:
        stock_item = (
            self.db.query(StockItem).filter(StockItem.id == stock_item_id).first()
        )
        return stock_item

    def get_all_stock_items(self) -> list[StockItem]:
        stock_items = self.db.query(StockItem).all()
        return stock_items

    def get_stock_item_by_name(self, stock_item_name: str) -> StockItem | None:
        stock_item = (
            self.db.query(StockItem).filter(StockItem.name == stock_item_name).first()
        )
        return stock_item

    def create_stock_item(self, create_stock_item_dto: CreateStockItemDto) -> StockItem:
        stock_item = self.get_stock_item_by_name(create_stock_item_dto.name)
        if stock_item:
            update_stock_item_dto = UpdateStockItemDto()
            update_stock_item_dto.quantity = (
                stock_item.quantity + create_stock_item_dto.quantity
            )
            stock_item = self.update_stock_item(stock_item.id, update_stock_item_dto)
            return stock_item
        if (
            self.item_category_service.get_item_category_by_id(
                create_stock_item_dto.category_id
            )
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id={create_stock_item_dto.category_id} not found",
            )
        stock_item = StockItem(**create_stock_item_dto.model_dump())
        current_date = datetime.now(timezone.utc)
        stock_item.creation_date = current_date
        stock_item.last_modification_date = current_date
        self.db.add(stock_item)
        self.db.commit()
        self.db.refresh(stock_item)
        return stock_item

    def update_stock_item(
        self,
        stock_item_id: int,
        update_stock_item_dto: UpdateStockItemDto,
    ) -> StockItem:
        stock_item = self.get_stock_item_by_id(stock_item_id)

        if stock_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock item with id={stock_item_id} not found",
            )
        current_date = datetime.now(timezone.utc)
        if update_stock_item_dto.name and stock_item.name != update_stock_item_dto.name:
            stock_item.name = update_stock_item_dto.name
            stock_item.last_modification_date = current_date
        if (
            update_stock_item_dto.description
            and stock_item.description != update_stock_item_dto.description
        ):
            stock_item.description = update_stock_item_dto.description
            stock_item.last_modification_date = current_date
        if (
            update_stock_item_dto.quantity
            and stock_item.quantity != update_stock_item_dto.quantity
        ):
            stock_item.quantity = update_stock_item_dto.quantity
            stock_item.last_modification_date = current_date
        if (
            update_stock_item_dto.category_id
            and stock_item.category_id != update_stock_item_dto.category_id
        ):
            if (
                self.item_category_service.get_item_category_by_id(
                    update_stock_item_dto.category_id
                )
                is None
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id={update_stock_item_dto.category_id} not found",
                )
            stock_item.category_id = update_stock_item_dto.category_id
            stock_item.last_modification_date = current_date

        self.db.commit()
        self.db.refresh(stock_item)
        return stock_item

    def delete_stock_item(self, stock_item_id: int) -> bool:
        stock_item = self.get_stock_item_by_id(stock_item_id)

        if stock_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock item with id={stock_item_id} not found",
            )
        self.db.delete(stock_item)
        self.db.commit()
        return True
