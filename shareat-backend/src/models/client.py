from decimal import Decimal
from sqlalchemy import ForeignKey, DECIMAL, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    hobbies: Mapped[str] = mapped_column(String, nullable=True)
    money: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=0)

    user: Mapped["User"] = relationship("User", back_populates="client")
