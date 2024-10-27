from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    secondname: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    client: Mapped["Client"] = relationship("Client", back_populates="user", uselist=False, lazy='selectin')
    admin: Mapped["Admin"] = relationship("Admin", back_populates="user", uselist=False, lazy='selectin')
    employee: Mapped["Employee"] = relationship("Employee", back_populates="user", uselist=False, lazy='selectin')
