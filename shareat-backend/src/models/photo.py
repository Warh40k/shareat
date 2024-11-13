from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class Photo(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    path: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="photos")
