from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from dependencies.dependencies import get_current_user, get_role_service
from exceptions.exceptions import RoleAlreadyExistsException, RoleNotFoundException
from models.models import (
    CreateRoleDto,
    PagedResult,
    ReadRoleDto,
    RoleFilterQuery,
    UpdateRoleDto,
)
from services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

service_dependency = Annotated[RoleService, Depends(get_role_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{role_id}", response_model=ReadRoleDto, status_code=status.HTTP_200_OK)
async def read_role(
    user: user_dependency, service: service_dependency, role_id: int = Path(gt=0)
):
    """
    Return a role by ID.
    Args:
        user: Current user dependency.
        service: Role service dependency.
        role_id (int): ID of the role to return.
    Returns:
        ReadRoleDto: Role data.
    Raises:
        HTTPException: If role is not found.
    """
    try:
        role = service.get_role_by_id(role_id)
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return role


@router.get("", response_model=PagedResult[ReadRoleDto], status_code=status.HTTP_200_OK)
async def read_all_roles(
    filter_query: Annotated[RoleFilterQuery, Query()],
    user: user_dependency,
    service: service_dependency,
):
    """
    Return a paginated list of roles with optional filtering.
    Args:
        filter_query (RoleFilterQuery): Filtering and pagination options.
        user: Current user dependency.
        service: Role service dependency.
    Returns:
        PagedResult[ReadRoleDto]: Paginated role data.
    """
    roles = service.get_all_roles(filter_query)
    return roles


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    user: user_dependency, service: service_dependency, role: CreateRoleDto
):
    """
    Create a new role.
    Args:
        user: Current user dependency.
        service: Role service dependency.
        role (CreateRoleDto): Data for the new role.
    Returns:
        str: Location of the created role resource.
    Raises:
        HTTPException: If role already exists.
    """
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
    """
    Update an existing role.
    Args:
        user: Current user dependency.
        service: Role service dependency.
        role (UpdateRoleDto): Data to update.
        role_id (int): ID of the role to update.
    Returns:
        str: Update confirmation message.
    Raises:
        HTTPException: If role not found or already exists.
    """
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
    """
    Delete a role by ID.
    Args:
        user: Current user dependency.
        service: Role service dependency.
        role_id (int): ID of the role to delete.
    Returns:
        str: Deletion confirmation message.
    Raises:
        HTTPException: If role not found.
    """
    try:
        service.delete_role(role_id)
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"Role with id={role_id} deleted."
