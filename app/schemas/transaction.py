from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: datetime
    category_id: int
    
class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
        
class CategorySummary(BaseModel):
    category_id: int
    total_amount: float
    class Config:
        from_attributes = True