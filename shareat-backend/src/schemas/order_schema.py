from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator

from src.models.order import OrderStatusEnum


class OrderBase(BaseModel):
    product_id: int
    user_id: Optional[int] = None
    status: Optional[OrderStatusEnum] = None
    start_date: date = None
    end_date: date
    total_price: Optional[Decimal] = None
    is_active: Optional[bool] = True

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if isinstance(value, int):  # Если приходит число, преобразуем в OrderStatusEnum
            return OrderStatusEnum.from_int(value)
        return value


class OrderCreate(BaseModel):
    product_id: int
    end_date: date

    @field_validator("end_date", mode="before")
    @classmethod
    def ensure_date(cls, value):
        """Приводим end_date к типу date."""
        if isinstance(value, str):
            return date.fromisoformat(value)
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        raise ValueError("Invalid date format")


class OrderUpdate(OrderBase):
    product_id: Optional[int] = None
    end_date: Optional[date] = None


class OrderRead(OrderBase):
    id: int

    @field_validator("status", mode="after")
    @classmethod
    def convert_status_to_int(cls, value: Optional[OrderStatusEnum]) -> Optional[int]:
        if isinstance(value, OrderStatusEnum):  # Преобразуем Enum обратно в число
            return value.to_int()
        return value

    class Config:
        from_attributes = True
