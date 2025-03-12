from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from database_settings import SessionLocal
from services.auth_service import AuthService
from services.item_category_service import ItemCategoryService
from services.role_service import RoleService
from services.stock_item_service import StockItemService
from services.user_service import UserService


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_stock_item_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> StockItemService:
    service = StockItemService(db)
    return service


def get_item_category_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> ItemCategoryService:
    service = ItemCategoryService(db)
    return service


def get_role_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> RoleService:
    service = RoleService(db)
    return service


def get_user_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> UserService:
    service = UserService(db)
    return service


def get_auth_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> AuthService:
    service = AuthService(db)
    return service
