from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database_settings import get_db_session

router = APIRouter(prefix="/roles", tags=["roles"])

db_session = Annotated[Session, Depends(get_db_session)]
