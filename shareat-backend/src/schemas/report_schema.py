from typing import Optional
from datetime import datetime


from pydantic import BaseModel


class ReportBase(BaseModel):
    type: str
    key: Optional[str]
    date: Optional[datetime]
    author_id: Optional[int]

class ReportCreate(ReportBase):
    key: str = None
    date: Optional[datetime] = None
    author_id: str = None

class ReportUpdate(ReportBase):
    type: Optional[str] = None
    author_id: Optional[str] = None
    key: Optional[str] = None

class ReportRead(ReportBase):
    pass

