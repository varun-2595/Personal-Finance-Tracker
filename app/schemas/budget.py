from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BudgetBase(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime
    category_id: int
    

class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True