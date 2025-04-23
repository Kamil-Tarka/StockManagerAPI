from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.exceptions import RoleAlreadyExistsException, RoleNotFoundException
from models.entities import Role
from models.models import CreateRoleDto, PagedResult, RoleFilterQuery, UpdateRoleDto
from paginate.paginate import paginate


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Role | None:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if role is None:
            raise RoleNotFoundException(f"Role with id={role_id} not found")
        return role

    def get_all_roles(self, filter_query: RoleFilterQuery) -> PagedResult:
        query = self.db.query(Role).filter(and_(*filter_query.filter_list))
        total_count = query.count()

        if filter_query.sort_by is not None and hasattr(Role, filter_query.sort_by):
            column = getattr(Role, filter_query.sort_by)
            if filter_query.sort_direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())
        roles = (
            query.offset((filter_query.page - 1) * filter_query.page_size)
            .limit(filter_query.page_size)
            .all()
        )
        paged_result = paginate(
            roles, filter_query.page, filter_query.page_size, total_count
        )
        return paged_result

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
            current_date = datetime.now(ZoneInfo("Europe/Warsaw"))
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
                role.last_modification_date = datetime.now(ZoneInfo("Europe/Warsaw"))
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

    def check_if_table_is_empty(self) -> bool:
        query = self.db.query(Role)
        if query.count() == 0:
            return True
        return False
