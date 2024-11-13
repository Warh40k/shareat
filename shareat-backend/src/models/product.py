from decimal import Decimal
from sqlalchemy import DECIMAL, Text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price_per_day: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    in_rent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="product",
                                                 cascade="all, delete-orphan", lazy='selectin')
