from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.exceptions import (
    StockItemAlreadyExistsException,
    StockItemNotFoundException,
)
from models.entities import ItemCategory, StockItem
from models.models import (
    CreateStockItemDto,
    PagedResult,
    StockItemQuery,
    UpdateStockItemDto,
)
from paginate.paginate import paginate
from services.item_category_service import ItemCategoryService

"""
Service for managing stock item operations, including CRUD, filtering, and business logic.
"""


class StockItemService:
    """
    Provides stock item management operations such as create, read, update, delete, and filtering.
    """

    def __init__(self, db: Session):
        """
        Initialize StockItemService with a database session.
        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db
        self.item_category_service = ItemCategoryService(db)

    def get_stock_item_by_id(self, stock_item_id: int) -> StockItem | None:
        """
        Return a stock item by its unique ID.
        Args:
            stock_item_id (int): The stock item's ID.
        Returns:
            StockItem: The stock item object if found.
        Raises:
            StockItemNotFoundException: If stock item is not found.
        """
        stock_item = (
            self.db.query(StockItem).filter(StockItem.id == stock_item_id).first()
        )
        if stock_item is None:
            raise StockItemNotFoundException(
                f"Stock item with id={stock_item_id} not found"
            )
        return stock_item

    def get_all_stock_items(self, filter_query: StockItemQuery) -> PagedResult:
        """
        Return all stock items matching the filter query, with pagination and sorting.
        Args:
            filter_query (StockItemQuery): Filtering and pagination options.
        Returns:
            PagedResult: Paginated result of stock items.
        """
        query = self.db.query(StockItem).filter(and_(*filter_query.filter_list))
        total_count = query.count()

        if filter_query.sort_by == "category":
            query = query.join(ItemCategory)
            if filter_query.sort_direction == "asc":
                query = query.order_by(ItemCategory.name.asc())
            else:
                query = query.order_by(ItemCategory.name.desc())
        elif filter_query.sort_by is not None and hasattr(
            StockItem, filter_query.sort_by
        ):
            column = getattr(StockItem, filter_query.sort_by)
            if filter_query.sort_direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())
        stock_items = (
            query.offset((filter_query.page - 1) * filter_query.page_size)
            .limit(filter_query.page_size)
            .all()
        )
        paged_result = paginate(
            stock_items, filter_query.page, filter_query.page_size, total_count
        )
        return paged_result

    def get_stock_item_by_name(self, stock_item_name: str) -> StockItem | None:
        """
        Return a stock item by its name.
        Args:
            stock_item_name (str): The stock item's name.
        Returns:
            StockItem: The stock item object if found.
        Raises:
            StockItemNotFoundException: If stock item is not found.
        """
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
        """
        Return a stock item by its name and category ID.
        Args:
            stock_item_name (str): The stock item's name.
            category_id (int): The category ID.
        Returns:
            StockItem: The stock item object if found.
        Raises:
            StockItemNotFoundException: If stock item is not found.
        """
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
        """
        Create a new stock item in the database.
        Args:
            create_stock_item_dto (CreateStockItemDto): Data for the new stock item.
        Returns:
            StockItem: The created stock item object.
        Raises:
            StockItemAlreadyExistsException: If stock item already exists.
        """
        try:
            stock_item = self.get_stock_item_by_name_and_category_id(
                create_stock_item_dto.name, create_stock_item_dto.category_id
            )
        except StockItemNotFoundException:
            self.item_category_service.get_item_category_by_id(
                create_stock_item_dto.category_id
            )

            stock_item = StockItem(**create_stock_item_dto.model_dump())
            current_date = datetime.now(ZoneInfo("Europe/Warsaw"))
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
        """
        Update an existing stock item's information.
        Args:
            stock_item_id (int): The stock item's ID.
            update_stock_item_dto (UpdateStockItemDto): Data to update.
        Returns:
            StockItem: The updated stock item object.
        Raises:
            StockItemAlreadyExistsException: If stock item already exists.
        """
        stock_item = self.get_stock_item_by_id(stock_item_id)
        current_date = datetime.now(ZoneInfo("Europe/Warsaw"))
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
        """
        Delete a stock item by its ID.
        Args:
            stock_item_id (int): The stock item's ID.
        Returns:
            bool: True if deletion was successful.
        """
        stock_item = self.get_stock_item_by_id(stock_item_id)

        self.db.delete(stock_item)
        self.db.commit()
        return True

    def check_if_table_is_empty(self) -> bool:
        """
        Check if the stock item table is empty.
        Returns:
            bool: True if empty, False otherwise.
        """
        query = self.db.query(StockItem)
        if query.count() == 0:
            return True
        return False
