from datetime import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from .base_model import Base


class OrderStatusEnum(str, PyEnum):
    new = "new"
    in_rent = "in_rent"
    returned = "returned"
    overdue = "overdue"
    completed = "completed"

    @classmethod
    def from_int(cls, value: int) -> "OrderStatusEnum":
        mapping = {
            1: cls.new,
            2: cls.in_rent,
            3: cls.returned,
            4: cls.overdue,
            5: cls.completed,
        }
        return mapping.get(value)

    def to_int(self) -> int:
        reverse_mapping = {
            OrderStatusEnum.new: 1,
            OrderStatusEnum.in_rent: 2,
            OrderStatusEnum.returned: 3,
            OrderStatusEnum.overdue: 4,
            OrderStatusEnum.completed: 5,
        }
        return reverse_mapping[self]


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum, name="order_status")
        , nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders", lazy="selectin")
    product: Mapped["Product"] = relationship("Product", lazy="selectin")

    transactions: Mapped["TransactionHistory"] = relationship("TransactionHistory", back_populates="order",
                                                              lazy="selectin")
