from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_roles_service
from services.roles_service import RolesService

router = APIRouter(prefix="/roles", tags=["roles"])

service_dependency = Annotated[RolesService, Depends(get_roles_service)]
