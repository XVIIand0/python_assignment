from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class financial_data(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    open_price: float
    close_price: float
    volume: float
    date: datetime