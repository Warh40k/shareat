from datetime import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class TransactionHistory(Base):
    __tablename__ = 'transaction_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    order_id: Mapped[int | None] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"), nullable=True)  # Сделано необязательным
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    delta_amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    order: Mapped["Order"] = relationship("Order", back_populates="transactions")
