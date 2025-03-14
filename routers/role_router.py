from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from dependencies.dependencies import get_current_user, get_role_service
from exceptions.exceptions import RoleAlreadyExistsException, RoleNotFoundException
from models.models import CreateRoleDto, ReadRoleDto, UpdateRoleDto
from services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

service_dependency = Annotated[RoleService, Depends(get_role_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{role_id}", response_model=ReadRoleDto, status_code=status.HTTP_200_OK)
async def read_role(
    user: user_dependency, service: service_dependency, role_id: int = Path(gt=0)
):
    try:
        role = service.get_role_by_id(role_id)
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return role


@router.get("", response_model=list[ReadRoleDto], status_code=status.HTTP_200_OK)
async def read_all_roles(user: user_dependency, service: service_dependency):
    roles = service.get_all_roles()
    return roles


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    user: user_dependency, service: service_dependency, role: CreateRoleDto
):
    try:
        created_role = service.create_role(role)
    except RoleAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"api/v1/roles/{created_role.id}"


@router.put("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_role(
    user: user_dependency,
    service: service_dependency,
    role: UpdateRoleDto,
    role_id: int = Path(gt=0),
):
    try:
        service.update_role(role_id, role)
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RoleAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"Role with id={role_id} updated."


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    user: user_dependency, service: service_dependency, role_id: int = Path(gt=0)
):
    try:
        service.delete_role(role_id)
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"Role with id={role_id} deleted."
