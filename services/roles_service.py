from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.entities import Roles
from models.models import CreateRoleDto, UpdateRoleDto


class RolesService:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Roles | None:
        role = self.db.query(Roles).filter(Roles.id == role_id).first()
        return role

    def get_all_roles(self) -> list[Roles]:
        roles = self.db.query(Roles).all()
        return roles

    def get_role_by_name(self, role_name: str) -> Roles | None:
        role = self.db.query(Roles).filter(Roles.name == role_name).first()
        return role

    def create_role(self, create_role_dto: CreateRoleDto) -> Roles:
        role = self.get_role_by_name(create_role_dto.name)
        if role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name={create_role_dto.name} already exists",
            )
        role = Roles(**create_role_dto.model_dump())
        current_date = datetime.now(timezone.utc)
        role.creation_date = current_date
        role.last_modification_date = current_date
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update_role(self, role_id: int, update_role_dto: UpdateRoleDto) -> Roles:
        role = self.get_role_by_id(self.db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id={role_id} not found",
            )
        if update_role_dto and role.name != update_role_dto.name:
            role.name = update_role_dto.name
            role.last_modification_date = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(role)
        return role

    def delete_role(self, role_id: int) -> Roles:
        role = self.get_role_by_id(self.db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id={role_id} not found",
            )
        self.db.delete(role)
        self.db.commit()
        return role
