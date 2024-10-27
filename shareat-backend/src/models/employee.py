from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    department: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)

    user: Mapped["User"] = relationship("User", back_populates="employee")
