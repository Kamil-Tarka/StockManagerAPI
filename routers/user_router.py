from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from dependencies.dependencies import get_current_user, get_user_service
from exceptions.exceptions import (
    RoleNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from models.models import CreateUserDto, ReadUserDto, UpdateUserDto
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

service_dependency = Annotated[UserService, Depends(get_user_service)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{user_id}", response_model=ReadUserDto, status_code=status.HTTP_200_OK)
async def read_user(
    user: user_dependency, service: service_dependency, user_id: int = Path(gt=0)
):
    try:
        get_user = service.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return get_user


@router.get("", response_model=list[ReadUserDto], status_code=status.HTTP_200_OK)
async def read_users(user: user_dependency, service: service_dependency):
    users = service.get_all_users()
    return users


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: user_dependency, service: service_dependency, create_user: CreateUserDto
):
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
    try:
        service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return f"User with id={user_id} deleted."
