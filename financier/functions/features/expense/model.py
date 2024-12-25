from pydantic import BaseModel
from datetime import datetime

class Expense(BaseModel):
    id: str
    name: str
    description: str | None
    amount: float
    quantity: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    tags: list[str]