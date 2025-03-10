from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_user_service
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

service_dependency = Annotated[UserService, Depends(get_user_service)]
