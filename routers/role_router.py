from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from dependencies.dependencies import get_current_user, get_role_service
from models.models import CreateRoleDto, ReadRoleDto, UpdateRoleDto
from services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

service_dependency = Annotated[RoleService, Depends(get_role_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{role_id}", response_model=ReadRoleDto, status_code=status.HTTP_200_OK)
async def read_role(
    user: user_dependency, service: service_dependency, role_id: int = Path(gt=0)
):
    role = service.get_role_by_id(role_id)
    return role


@router.get("", response_model=list[ReadRoleDto], status_code=status.HTTP_200_OK)
async def read_all_roles(user: user_dependency, service: service_dependency):
    roles = service.get_all_roles()
    return roles


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    user: user_dependency, service: service_dependency, role: CreateRoleDto
):
    created_role = service.create_role(role)
    return f"api/v1/roles/{created_role.id}"


@router.put("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_role(
    user: user_dependency,
    service: service_dependency,
    role: UpdateRoleDto,
    role_id: int = Path(gt=0),
):
    service.update_role(role_id, role)
    return f"Role with id={role_id} updated."


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    user: user_dependency, service: service_dependency, role_id: int = Path(gt=0)
):
    service.delete_role(role_id)
    return f"Role with id={role_id} deleted."
