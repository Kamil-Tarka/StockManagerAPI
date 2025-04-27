from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_settings import SessionLocal
from services.auth_service import AuthService
from services.item_category_service import ItemCategoryService
from services.role_service import RoleService
from services.stock_item_service import StockItemService
from services.user_service import UserService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db_session() -> AsyncGenerator[Session, None]:
    """
    Dependency that provides a SQLAlchemy database session.
    Yields a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_stock_item_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> StockItemService:
    """
    Dependency that provides a StockItemService instance using the database session.
    """
    service = StockItemService(db)
    return service


async def get_item_category_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> ItemCategoryService:
    """
    Dependency that provides an ItemCategoryService instance using the database session.
    """
    service = ItemCategoryService(db)
    return service


async def get_role_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> RoleService:
    """
    Dependency that provides a RoleService instance using the database session.
    """
    service = RoleService(db)
    return service


async def get_user_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> UserService:
    """
    Dependency that provides a UserService instance using the database session.
    """
    service = UserService(db)
    return service


async def get_auth_service(
    db: Annotated[Session, Depends(get_db_session)],
) -> AuthService:
    """
    Dependency that provides an AuthService instance using the database session.
    """
    service = AuthService(db)
    return service


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    Dependency that retrieves the current user based on the provided OAuth2 token.
    Uses the AuthService to validate and return the user.
    """
    return service.get_current_user(token)
