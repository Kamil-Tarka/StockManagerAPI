from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.dependencies import get_role_service
from models.models import CreateRoleDto, ReadRoleDto, UpdateRoleDto
from services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

service_dependency = Annotated[RoleService, Depends(get_role_service)]


@router.get("/{role_id}", response_model=ReadRoleDto, status_code=status.HTTP_200_OK)
async def read_role(service: service_dependency, role_id: int):
    role = service.get_role_by_id(role_id)
    return role


@router.get("", response_model=list[ReadRoleDto], status_code=status.HTTP_200_OK)
async def read_all_roles(service: service_dependency):
    roles = service.get_all_roles()
    return roles


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(service: service_dependency, role: CreateRoleDto):
    created_role = service.create_role(role)
    return f"api/v1/roles/{created_role.id}"


@router.put("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_role(service: service_dependency, role: UpdateRoleDto, role_id: int):
    service.update_role(role_id, role)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(service: service_dependency, role_id: int):
    service.delete_role(role_id)
