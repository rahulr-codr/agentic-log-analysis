from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class QuoteBase(BaseModel):
    text: str
    author: str


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(QuoteBase):
    text: Optional[str] = None
    author: Optional[str] = None


class Quote(QuoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
