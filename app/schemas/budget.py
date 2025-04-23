from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class BudgetBase(BaseModel):
    amount: float
    start_date: datetime
    end_date: datetime
    category_id: int
    period: str
    
    @validator("start_date")
    def end_date_must_be_after_start_date(cls, v, values):
        if "end_date" in values and v >= values["end_date"]:
            raise ValueError("start_date must be before end_date")
        return v
    
    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v
    

class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True