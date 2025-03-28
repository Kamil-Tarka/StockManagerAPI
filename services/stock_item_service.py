from datetime import datetime, timezone

from sqlalchemy.orm import Session

from exceptions.exceptions import (
    StockItemAlreadyExistsException,
    StockItemNotFoundException,
)
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
        if stock_item is None:
            raise StockItemNotFoundException(
                f"Stock item with id={stock_item_id} not found"
            )
        return stock_item

    def get_all_stock_items(self) -> list[StockItem]:
        stock_items = self.db.query(StockItem).all()
        return stock_items

    def get_stock_item_by_name(self, stock_item_name: str) -> StockItem | None:
        stock_item = (
            self.db.query(StockItem).filter(StockItem.name == stock_item_name).first()
        )
        if stock_item is None:
            raise StockItemNotFoundException(
                f"Stock item with name={stock_item_name} not found"
            )
        return stock_item

    def get_stock_item_by_name_and_category_id(
        self, stock_item_name: str, category_id: int
    ) -> StockItem | None:
        stock_item = (
            self.db.query(StockItem)
            .filter(
                StockItem.name == stock_item_name, StockItem.category_id == category_id
            )
            .first()
        )
        if stock_item is None:
            raise StockItemNotFoundException(
                f"Stock item with name={stock_item_name} and category_id={category_id} not found"
            )
        return stock_item

    def create_stock_item(self, create_stock_item_dto: CreateStockItemDto) -> StockItem:
        try:
            stock_item = self.get_stock_item_by_name_and_category_id(
                create_stock_item_dto.name, create_stock_item_dto.category_id
            )
        except StockItemNotFoundException:
            self.item_category_service.get_item_category_by_id(
                create_stock_item_dto.category_id
            )

            stock_item = StockItem(**create_stock_item_dto.model_dump())
            current_date = datetime.now(timezone.utc)
            stock_item.creation_date = current_date
            stock_item.last_modification_date = current_date
            self.db.add(stock_item)
            self.db.commit()
            self.db.refresh(stock_item)
            return stock_item
        else:
            raise StockItemAlreadyExistsException(
                f"Stock item with name={create_stock_item_dto.name} already exists"
            )

    def update_stock_item(
        self,
        stock_item_id: int,
        update_stock_item_dto: UpdateStockItemDto,
    ) -> StockItem:
        stock_item = self.get_stock_item_by_id(stock_item_id)
        current_date = datetime.now(timezone.utc)
        if update_stock_item_dto.name and stock_item.name != update_stock_item_dto.name:
            try:
                self.get_stock_item_by_name_and_category_id(
                    update_stock_item_dto.name, update_stock_item_dto.category_id
                )
            except StockItemNotFoundException:
                stock_item.name = update_stock_item_dto.name
                stock_item.last_modification_date = current_date
            else:
                raise StockItemAlreadyExistsException(
                    f"Stock item with name={update_stock_item_dto.name} already exists"
                )
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
            self.item_category_service.get_item_category_by_id(
                update_stock_item_dto.category_id
            )
            stock_item.category_id = update_stock_item_dto.category_id
            stock_item.last_modification_date = current_date
        self.db.commit()
        self.db.refresh(stock_item)
        return stock_item

    def delete_stock_item(self, stock_item_id: int) -> bool:
        stock_item = self.get_stock_item_by_id(stock_item_id)

        self.db.delete(stock_item)
        self.db.commit()
        return True
