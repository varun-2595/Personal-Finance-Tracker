from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.budget import BudgetCreate, Budget
from app.api.crud.budget import create_budget, get_budget, get_user_budgets, update_budget, delete_budget, get_budget_statistics
from app.api.auth import get_current_user, get_current_active_user


router = APIRouter()

@router.post("/", response_model=Budget, status_code=201)
def create_budget_endpoint(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> Budget:
    db_budget = create_budget(db, budget, current_user.id)
    if not db_budget:
        raise HTTPException(status_code=400, detail="Category not found")
    return db_budget


@router.get("/{budget_id}", response_model=Budget)
def read_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> Budget:
    db_budget = get_budget(db, budget_id, current_user.id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget


@router.get("/", response_model=List[Budget])
def read_budgets(
    db: Session = Depends(get_db),
    active_only: bool = False,
    category_id: Optional[int] = None,
    current_user: int = Depends(get_current_user),
) -> List[Budget]:
    return get_user_budgets(db, current_user.id, category_id, active_only)


@router.put("/{budget_id}", response_model=Budget)
def update_budget_endpoint(
    budget_id: int,
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> Budget:
    db_budget = update_budget(db, budget_id, budget, current_user.id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found or category not found")
    return db_budget


@router.delete("/{budget_id}", response_model=dict)  # Change response_model to dict
def delete_budget_endpoint(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete a budget for the current user.
    """
    success = delete_budget(db=db, budget_id=budget_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"detail": "Budget deleted successfully"}


@router.get("/statistics/spending-vs-budget", response_model=List[Budget])
def get_spending_vs_budget(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
) -> List[Budget]:
    """
    Endpoint to get spending vs budget statistics for the current user.
    """
    return get_budget_statistics(db, current_user.id)