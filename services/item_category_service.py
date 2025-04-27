from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.exceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
)
from models.entities import ItemCategory
from models.models import (
    CreateItemCategoryDto,
    ItemCategoryFilterQuery,
    PagedResult,
    UpdateItemCategoryDto,
)
from paginate.paginate import paginate

"""
Service for managing item category operations, including CRUD, filtering, and business logic.
"""


class ItemCategoryService:
    """
    Provides item category management operations such as create, read, update, delete, and filtering.
    """

    def __init__(self, db: Session):
        """
        Initialize ItemCategoryService with a database session.
        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db

    def get_item_category_by_id(self, item_category_id: int) -> ItemCategory | None:
        """
        Return an item category by its unique ID.
        Args:
            item_category_id (int): The item category's ID.
        Returns:
            ItemCategory: The item category object if found.
        Raises:
            CategoryNotFoundException: If item category is not found.
        """
        item_category = (
            self.db.query(ItemCategory)
            .filter(ItemCategory.id == item_category_id)
            .first()
        )
        if item_category is None:
            raise CategoryNotFoundException(
                f"Item category with id={item_category_id} not found"
            )
        return item_category

    def get_all_item_categories(
        self, filter_query: ItemCategoryFilterQuery
    ) -> PagedResult:
        """
        Return all item categories matching the filter query, with pagination and sorting.
        Args:
            filter_query (ItemCategoryFilterQuery): Filtering and pagination options.
        Returns:
            PagedResult: Paginated result of item categories.
        """
        query = self.db.query(ItemCategory).filter(and_(*filter_query.filter_list))
        total_count = query.count()

        if filter_query.sort_by is not None and hasattr(
            ItemCategory, filter_query.sort_by
        ):
            column = getattr(ItemCategory, filter_query.sort_by)
            if filter_query.sort_direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())

        item_categories = (
            query.offset((filter_query.page - 1) * filter_query.page_size)
            .limit(filter_query.page_size)
            .all()
        )
        paged_result = paginate(
            item_categories, filter_query.page, filter_query.page_size, total_count
        )
        return paged_result

    def get_category_by_name(self, category_name: str) -> ItemCategory | None:
        """
        Return an item category by its name.
        Args:
            category_name (str): The item category's name.
        Returns:
            ItemCategory: The item category object if found.
        Raises:
            CategoryNotFoundException: If item category is not found.
        """
        item_category = (
            self.db.query(ItemCategory)
            .filter(ItemCategory.name == category_name)
            .first()
        )
        if item_category is None:
            raise CategoryNotFoundException(
                f"Item category with name={category_name} not found"
            )
        return item_category

    def create_item_category(
        self, create_item_category: CreateItemCategoryDto
    ) -> ItemCategory:
        """
        Create a new item category in the database.
        Args:
            create_item_category (CreateItemCategoryDto): Data for the new item category.
        Returns:
            ItemCategory: The created item category object.
        Raises:
            CategoryAlreadyExistsException: If item category already exists.
        """
        try:
            item_category = self.get_category_by_name(create_item_category.name)
        except CategoryNotFoundException:
            item_category = ItemCategory(**create_item_category.model_dump())
            current_date = datetime.now(ZoneInfo("Europe/Warsaw"))
            item_category.creation_date = current_date
            item_category.last_modification_date = current_date
            self.db.add(item_category)
            self.db.commit()
            self.db.refresh(item_category)
            return item_category
        else:
            raise CategoryAlreadyExistsException(
                f"Item category with name={create_item_category.name} already exists"
            )

    def update_category(
        self,
        category_id: int,
        update_item_category_dto: UpdateItemCategoryDto,
    ) -> ItemCategory:
        """
        Update an existing item category's information.
        Args:
            category_id (int): The item category's ID.
            update_item_category_dto (UpdateItemCategoryDto): Data to update.
        Returns:
            ItemCategory: The updated item category object.
        Raises:
            CategoryAlreadyExistsException: If item category already exists.
        """
        item_category = self.get_item_category_by_id(category_id)
        try:
            self.get_category_by_name(update_item_category_dto.name)
        except CategoryNotFoundException:
            if (
                update_item_category_dto.name
                and item_category.name != update_item_category_dto.name
            ):
                item_category.name = update_item_category_dto.name
                item_category.last_modification_date = datetime.now(
                    ZoneInfo("Europe/Warsaw")
                )
                self.db.commit()
                self.db.refresh(item_category)
        else:
            raise CategoryAlreadyExistsException(
                f"Item category with name={update_item_category_dto.name} already exists"
            )
        return item_category

    def delete_category(self, category_id: int) -> bool:
        """
        Delete an item category by its ID.
        Args:
            category_id (int): The item category's ID.
        Returns:
            bool: True if deletion was successful.
        """
        item_category = self.get_item_category_by_id(category_id)

        self.db.delete(item_category)
        self.db.commit()
        return True

    def check_if_table_is_empty(self) -> bool:
        """
        Check if the item category table is empty.
        Returns:
            bool: True if empty, False otherwise.
        """
        query = self.db.query(ItemCategory)
        if query.count() == 0:
            return True
        return False
