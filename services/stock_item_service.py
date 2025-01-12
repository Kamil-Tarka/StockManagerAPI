from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.entities import StockItem
from models.models import CreateStockItemDto, UpdateStockItemDto
from services.item_category_service import ItemCategoryService


class StockItemService:

    def get_stock_item_by_id(self, db: Session, stock_item_id: int) -> StockItem | None:
        stock_item = db.query(StockItem).filter(StockItem.id == stock_item_id).first()
        return stock_item

    def get_all_stock_items(self, db: Session) -> list[StockItem]:
        stock_items = db.query(StockItem).all()
        return stock_items

    def get_stock_item_by_name(
        self, db: Session, stock_item_name: str
    ) -> StockItem | None:
        stock_item = (
            db.query(StockItem).filter(StockItem.name == stock_item_name).first()
        )
        return stock_item

    def create_stock_item(
        self, db: Session, create_stock_item_dto: CreateStockItemDto
    ) -> StockItem:
        stock_item = self.get_stock_item_by_name(db, create_stock_item_dto.name)
        if stock_item:
            update_stock_item_dto = UpdateStockItemDto()
            update_stock_item_dto.amount = (
                stock_item.amount + create_stock_item_dto.amount
            )
            stock_item = self.update_stock_item(
                db, stock_item.id, update_stock_item_dto
            )
            return stock_item
        if (
            ItemCategoryService.get_item_category_by_id(
                db, create_stock_item_dto.category_id
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
        db.add(stock_item)
        db.commit()
        db.refresh(stock_item)
        return stock_item

    def update_stock_item(
        self,
        db: Session,
        stock_item_id: int,
        update_stock_item_dto: UpdateStockItemDto,
    ) -> StockItem:
        stock_item = self.get_stock_item_by_id(db, stock_item_id)

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
            update_stock_item_dto.amount
            and stock_item.amount != update_stock_item_dto.amount
        ):
            stock_item.amount = update_stock_item_dto.amount
            stock_item.last_modification_date = current_date
        if (
            update_stock_item_dto.category_id
            and stock_item.category_id != update_stock_item_dto.category_id
        ):
            if (
                ItemCategoryService.get_item_category_by_id(
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

        db.commit()
        db.refresh(stock_item)
        return stock_item

    def delete_stock_item(self, db: Session, stock_item_id: int) -> bool:
        stock_item = self.get_stock_item_by_id(db, stock_item_id)

        if stock_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock item with id={stock_item_id} not found",
            )
        db.delete(stock_item)
        return True


def get_stock_item_service() -> StockItemService:
    service = StockItemService()
    return service
