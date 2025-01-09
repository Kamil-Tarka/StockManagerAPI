from datetime import datetime, timezone

from sqlalchemy.orm import Session

from exceptions.exceptions import CategoryNotFoundError
from models.entities import ItemCategory
from models.models import CreateItemCategoryDto, UpdateItemCategoryDto


class ItemCategoryService:

    def get_item_category_by_id(
        self, db: Session, item_category_id: int
    ) -> ItemCategory | None:
        item_category = (
            db.query(ItemCategory).filter(ItemCategory.id == item_category_id).first()
        )
        return item_category

    def get_all_item_categories(self, db: Session) -> list[ItemCategory]:
        item_categories = db.query(ItemCategory).all()
        return item_categories

    def get_category_by_name(
        self, db: Session, category_name: str
    ) -> ItemCategory | None:
        item_category = (
            db.query(ItemCategory).filter(ItemCategory.name == category_name).first()
        )
        return item_category

    def create_item_category(
        self, db: Session, create_item_category: CreateItemCategoryDto
    ) -> ItemCategory:

        item_category = self.get_category_by_name(db, create_item_category.name)

        if item_category:
            return item_category

        item_category = ItemCategory(**create_item_category.model_dump())
        current_date = datetime.now(timezone.utc)
        item_category.creation_date = current_date
        item_category.last_modification_date = current_date
        db.add(item_category)
        db.commit()
        db.refresh(item_category)
        return item_category

    def update_category(
        self,
        db: Session,
        category_id: int,
        update_item_category_dto: UpdateItemCategoryDto,
    ) -> ItemCategory:
        item_category = self.get_item_category_by_id(db, category_id)

        if item_category is None:
            raise CategoryNotFoundError(
                f"Item category with id={category_id} not found"
            )

        if (
            update_item_category_dto.name
            and item_category.name != update_item_category_dto.name
        ):
            item_category.name = update_item_category_dto.name
            item_category.last_modification_date = datetime.now(timezone.utc)
            db.commit()
            db.refresh(item_category)

        return item_category

    def delete_category(self, db: Session, category_id: int) -> bool:
        item_category = self.get_item_category_by_id(db, category_id)

        if item_category is None:
            raise CategoryNotFoundError(
                f"Item category with id={category_id} not found"
            )
        db.delete(item_category)
        return True


def get_item_category_service() -> ItemCategoryService:
    service = ItemCategoryService()
    return service
