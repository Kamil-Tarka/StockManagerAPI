from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from exceptions.exceptions import CategoryNotFoundError
from models.entities import ItemCategory
from models.models import CreateItemCategoryDto, UpdateItemCategoryDto


class ItemCategoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_item_category_by_id(self, item_category_id: int) -> ItemCategory | None:
        item_category = (
            self.db.query(ItemCategory)
            .filter(ItemCategory.id == item_category_id)
            .first()
        )
        return item_category

    def get_all_item_categories(self) -> list[ItemCategory]:
        item_categories = self.db.query(ItemCategory).all()
        return item_categories

    def get_category_by_name(self, category_name: str) -> ItemCategory | None:
        item_category = (
            self.db.query(ItemCategory)
            .filter(ItemCategory.name == category_name)
            .first()
        )
        return item_category

    def create_item_category(
        self, create_item_category: CreateItemCategoryDto
    ) -> ItemCategory:

        item_category = self.get_category_by_name(self.db, create_item_category.name)

        if item_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item category with name={create_item_category.name} already exists",
            )

        item_category = ItemCategory(**create_item_category.model_dump())
        current_date = datetime.now(timezone.utc)
        item_category.creation_date = current_date
        item_category.last_modification_date = current_date
        self.db.add(item_category)
        self.db.commit()
        self.db.refresh(item_category)
        return item_category

    def update_category(
        self,
        category_id: int,
        update_item_category_dto: UpdateItemCategoryDto,
    ) -> ItemCategory:
        item_category = self.get_item_category_by_id(category_id)

        if item_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item category with id={category_id} not found",
            )

        if (
            update_item_category_dto.name
            and item_category.name != update_item_category_dto.name
        ):
            item_category.name = update_item_category_dto.name
            item_category.last_modification_date = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(item_category)

        return item_category

    def delete_category(self, category_id: int) -> bool:
        item_category = self.get_item_category_by_id(category_id)

        if item_category is None:
            raise CategoryNotFoundError(
                f"Item category with id={category_id} not found"
            )
        self.db.delete(item_category)
        self.db.commit()
        return True
