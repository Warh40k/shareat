from decimal import Decimal
from typing import Optional, Union

from fastapi_users import schemas
from pydantic import BaseModel


class ClientRead(BaseModel):
    address: str | None = None
    phone_number: str | None = None
    hobbies: str | None = None
    money: Decimal | None = None

    class Config:
        from_attributes = True


class AdminRead(BaseModel):
    department: str | None = None

    class Config:
        from_attributes = True


class EmployeeRead(BaseModel):
    department: str | None = None
    position: str | None = None

    class Config:
        from_attributes = True


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str | None = None
    firstname: str | None = None
    secondname: str | None = None
    email: str | None = None
    role_id: int | None = 1
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    firstname: str
    secondname: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str = None
    firstname: str = None
    secondname: str = None
    role_id: int = None
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class ResetPasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UserDetails(UserRead):
    # Поля клиента (опционально)
    address: Optional[str] = None
    phone_number: Optional[str] = None
    hobbies: Optional[str] = None
    money: Optional[Decimal] = None

    # Поля админа (опционально)
    department: Optional[str] = None

    # Поля работника (опционально)
    position: Optional[str] = None

    class Config:
        from_attributes = True  # Включаем поддержку работы с ORM
        exclude_unset = True  # Исключаем поля со значением None
        exclude_none = True
