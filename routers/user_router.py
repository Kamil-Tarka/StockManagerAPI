from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from dependencies.dependencies import get_current_user, get_user_service
from exceptions.exceptions import (
    RoleNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from models.models import (
    CreateUserDto,
    PagedResult,
    ReadUserDto,
    UpdateUserDto,
    UserFilterQuery,
)
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

service_dependency = Annotated[UserService, Depends(get_user_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{user_id}", response_model=ReadUserDto, status_code=status.HTTP_200_OK)
async def read_user(
    user: user_dependency, service: service_dependency, user_id: int = Path(gt=0)
):
    """
    Return a user by ID.
    Args:
        user: Current user dependency.
        service: User service dependency.
        user_id (int): ID of the user to return.
    Returns:
        ReadUserDto: User data.
    Raises:
        HTTPException: If user is not found.
    """
    try:
        get_user = service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return get_user


@router.get("", response_model=PagedResult[ReadUserDto], status_code=status.HTTP_200_OK)
async def read_users(
    filter_query: Annotated[UserFilterQuery, Query()],
    user: user_dependency,
    service: service_dependency,
):
    """
    Return a paginated list of users with optional filtering.
    Args:
        filter_query (UserFilterQuery): Filtering and pagination options.
        user: Current user dependency.
        service: User service dependency.
    Returns:
        PagedResult[ReadUserDto]: Paginated user data.
    """
    users = service.get_all_users(filter_query)

    return users


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: user_dependency, service: service_dependency, create_user: CreateUserDto
):
    """
    Create a new user.
    Args:
        user: Current user dependency.
        service: User service dependency.
        create_user (CreateUserDto): Data for the new user.
    Returns:
        str: Location of the created user resource.
    Raises:
        HTTPException: If user already exists or role not found.
    """
    try:
        created_user = service.create_user(create_user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return f"api/v1/users/{created_user.id}"


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user: user_dependency,
    service: service_dependency,
    update_user: UpdateUserDto,
    user_id: int = Path(gt=0),
):
    """
    Update an existing user.
    Args:
        user: Current user dependency.
        service: User service dependency.
        update_user (UpdateUserDto): Data to update.
        user_id (int): ID of the user to update.
    Returns:
        str: Update confirmation message.
    Raises:
        HTTPException: If user not found, role not found, or user already exists.
    """
    try:
        service.update_user(user_id, update_user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RoleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return f"User with id={user_id} updated."


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: user_dependency, service: service_dependency, user_id: int = Path(gt=0)
):
    """
    Delete a user by ID.
    Args:
        user: Current user dependency.
        service: User service dependency.
        user_id (int): ID of the user to delete.
    Returns:
        str: Deletion confirmation message.
    Raises:
        HTTPException: If user not found.
    """
    try:
        service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"User with id={user_id} deleted."
