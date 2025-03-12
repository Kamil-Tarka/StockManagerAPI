import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database_settings import Base


class ItemCategory(Base):
    __tablename__ = "item_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_modification_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    stock_item: Mapped[List["StockItem"]] = relationship(
        "StockItem", back_populates="category"
    )


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_modification_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    role_users: Mapped[list["User"]] = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        ForeignKeyConstraint(["role_id"], ["role.id"], name="fk_User_Role_id"),
        Index("fk_User_Role_id", "role_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[int] = mapped_column(Boolean)
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_modification_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    role_id: Mapped[int] = mapped_column(Integer)
    role: Mapped["Role"] = relationship("Role", back_populates="role_users")


class StockItem(Base):
    __tablename__ = "stock_item"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"], ["item_category.id"], name="fk_StockItem_category_id"
        ),
        Index("fk_StockItem_category_id", "category_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer)
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_modification_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    description: Mapped[Optional[str]] = mapped_column(Text)

    category: Mapped["ItemCategory"] = relationship(
        "ItemCategory", back_populates="stock_item"
    )
