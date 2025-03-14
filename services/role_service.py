from datetime import datetime, timezone

from sqlalchemy.orm import Session

from exceptions.exceptions import RoleAlreadyExistsException, RoleNotFoundException
from models.entities import Role
from models.models import CreateRoleDto, UpdateRoleDto


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Role | None:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise RoleNotFoundException(f"Role with id={role_id} not found")
        return role

    def get_all_roles(self) -> list[Role]:
        roles = self.db.query(Role).all()
        return roles

    def get_role_by_name(self, role_name: str) -> Role | None:
        role = self.db.query(Role).filter(Role.name == role_name).first()
        if role is None:
            raise RoleNotFoundException(f"Role with name={role_name} not found")
        return role

    def create_role(self, create_role_dto: CreateRoleDto) -> Role:
        try:
            role = self.get_role_by_name(create_role_dto.name)
        except RoleNotFoundException:
            role = Role(**create_role_dto.model_dump())
            current_date = datetime.now(timezone.utc)
            role.creation_date = current_date
            role.last_modification_date = current_date
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        else:
            raise RoleAlreadyExistsException(
                f"Role with name={create_role_dto.name} already exists"
            )

    def update_role(self, role_id: int, update_role_dto: UpdateRoleDto) -> Role:
        role = self.get_role_by_id(role_id)
        try:
            self.get_role_by_name(update_role_dto.name)
        except RoleNotFoundException:
            if update_role_dto and role.name != update_role_dto.name:
                role.name = update_role_dto.name
                role.last_modification_date = datetime.now(timezone.utc)
                self.db.commit()
                self.db.refresh(role)
            return role
        else:
            raise RoleAlreadyExistsException(
                f"Role with name={update_role_dto.name} already exists"
            )

    def delete_role(self, role_id: int) -> Role:
        role = self.get_role_by_id(role_id)

        self.db.delete(role)
        self.db.commit()
        return role
