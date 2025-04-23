from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.db.models import Budget, Category, Transaction
from app.schemas.budget import BudgetCreate


def create_budget(db: Session, budget: BudgetCreate, user_id: int) -> Budget:
    category = db.query(Category).filter(Category.id == budget.category_id, Category.user_id == user_id).first()
    if not category:
        return None
    db_budget = Budget(
        amount=budget.amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
        category_id=budget.category_id,
        user_id=user_id,
        period = budget.period,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def get_budget(db: Session, budget_id: int, user_id: int) -> Optional[Budget]:
    return db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()


def get_user_budgets(db: Session, user_id: int, category_id: Optional[int] = None, active_only: bool = False) -> List[Budget]:
    query = db.query(Budget).filter(Budget.user_id == user_id)
    if category_id:
        query = query.filter(Budget.category_id == category_id)
    if active_only:
        current_date = datetime.utcnow()
        query = query.filter(Budget.start_date <= current_date, Budget.end_date >= current_date)
    return query.all()


def update_budget(db: Session, budget_id: int, budget: BudgetCreate, user_id: int) -> Optional[Budget]:
    db_budget = get_budget(db, budget_id, user_id)
    if not db_budget:
        return None
    category = db.query(Category).filter(Category.id == budget.category_id, Category.user_id == user_id).first()
    if not category:
        return None
    db_budget.amount = budget.amount
    db_budget.start_date = budget.start_date
    db_budget.end_date = budget.end_date
    db_budget.category_id = budget.category_id
    db_budget.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_budget)
    return db_budget


def delete_budget(db: Session, budget_id: int, user_id: int) -> Optional[Budget]:
    db_budget = get_budget(db, budget_id, user_id)
    if not db_budget:
        return False
    db.delete(db_budget)
    db.commit()
    return db_budget


def get_budget_statistics(db: Session, user_id: int, month: Optional[int] = None, year: Optional[int] = None) -> List[Budget]:
    if not month or not year:
        current_date = datetime.utcnow()
        month = month or current_date.month
        year = year or current_date.year
        
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
        
    budgets = db.query(Budget).filter(Budget.user_id == user_id, Budget.start_date >= start_date, Budget.end_date < end_date).all()
    
    results = []
    for budget in budgets:
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.category_id == budget.category_id,
            Transaction.date >= start_date,
            Transaction.date < end_date,
            Transaction.user_id == user_id
        ).scalar() or 0
        
        category = db.query(Category).filter(Category.id == budget.category_id, Category.user_id == user_id).first()
        if category:
            budget_data = {
                "budget_id": budget.id,
                "category_id": budget.category_id,
                "category_name": category.name,
                "budget_amount": budget.amount,
                "spent_amount": float(total_spent),
                "remaining_amount": float(budget.amount - total_spent),
                "percentage_spent": float((total_spent / budget.amount) * 100) if budget.amount > 0 else 0
            }
            results.append(budget_data)
            
    return results