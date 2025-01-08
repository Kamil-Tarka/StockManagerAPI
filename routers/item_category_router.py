from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database_settings import get_db_session

router = APIRouter(prefix="/item-categories", tags=["item-categories"])

db_session = Annotated[Session, Depends(get_db_session)]
