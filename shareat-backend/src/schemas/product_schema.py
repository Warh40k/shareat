from typing import Optional, List

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price_per_day: int
    in_rent: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    title: str = None
    price_per_day: int = None


class ProductRead(ProductBase):
    id: int
    photos: Optional[List[str]] = None
