from sqlalchemy.orm import Session

from database_settings import SessionLocal
from exceptions.exceptions import RoleNotCreatedException, UserNotCreatedException
from models.models import CreateRoleDto, CreateUserDto
from services.item_category_service import ItemCategoryService
from services.role_service import RoleService
from services.stock_item_service import StockItemService
from services.user_service import UserService


class AppInitializer:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.user_service = UserService(self.db)
        self.role_service = RoleService(self.db)
        self.item_category_service = ItemCategoryService(self.db)
        self.stock_item_service = StockItemService(self.db)

    def verify_if_tables_have_content(self):
        users_is_empty = self.user_service.check_if_table_is_empty()
        roles_is_empty = self.role_service.check_if_table_is_empty()
        item_categories_is_empty = self.item_category_service.check_if_table_is_empty()
        stock_items_is_empty = self.stock_item_service.check_if_table_is_empty()
        if (
            users_is_empty
            and roles_is_empty
            and item_categories_is_empty
            and stock_items_is_empty
        ):
            return False
        return True

    def seed(self):
        create_admin_role_dto = CreateRoleDto(
            name="admin",
            description="Administrator role with full access",
        )
        user_name = input('Enter administrator user name(default is "admin"): ')
        if not user_name:
            user_name = "admin"
        user_password = input('Enter administrator password(default is "admin123"): ')
        if not user_password:
            user_password = "admin123"
        first_name = input('Enter administrator first name(default is "Admin"): ')
        if not first_name:
            first_name = "Admin"
        last_name = input('Enter administrator last name(default is "User"): ')
        if not last_name:
            last_name = "User"
        email = input('Enter administrator email(default is "admin@local.com"): ')
        if not email:
            email = "admin@local.com"

        admin_role = self.role_service.create_role(create_admin_role_dto)
        if not admin_role:
            raise RoleNotCreatedException("Failed to create admin role")

        create_user_dto = CreateUserDto(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=user_password,
            role_id=admin_role.id,
        )
        user = self.user_service.create_user(create_user_dto)
        if not user:
            raise UserNotCreatedException("Failed to create admin user")
        print("#################################################")
        print(f"Admin user {user.user_name} created with role {admin_role.name}")
        print("#################################################")

    def initialize(self):
        if not self.verify_if_tables_have_content():
            print("Database is empty, please provide required information")
            return self.seed()
        self.db.close()
