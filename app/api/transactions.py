from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.schemas.transaction import Transaction, TransactionCreate, CategorySummary
from app.api.crud.transaction import create_transaction, get_transactions, get_user_transactions, update_transaction, delete_transaction
from app.api.auth import get_current_active_user


router = APIRouter()

@router.post("/", response_model=Transaction)
def create_transaction_endpoint(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Create a new transaction for the current user.
    """
    return create_transaction(db=db, transaction=transaction, user_id=current_user.id)


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Retrieve a transaction by ID for the current user.
    """
    transaction = get_transactions(db=db, transaction_id=transaction_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/", response_model=List[Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Endpoint to list transactions for the current user with optional filters.
    """
    transactions = get_user_transactions(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id
    )
    return transactions


@router.put("/{transaction_id}", response_model=Transaction)
def update_existing_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Update an existing transaction for the current user.
    """
    updated_transaction = update_transaction(db=db, transaction_id=transaction_id, transaction=transaction)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction


@router.delete("/{transaction_id}", response_model=dict)
def delete_existing_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Delete a transaction for the current user.
    """
    success = delete_transaction(db=db, transaction_id=transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}


@router.get("/summary/by-category", response_model=List[CategorySummary])
def get_transactions_by_category(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Get transaction totals grouped by category for the current user.
    """
    query = db.query(
        Transaction.category_id,
        func.sum(Transaction.amount).label("total_amount")
    ).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
        
    return query.group_by(Transaction.category_id).all()


@router.get("/summary/monthly")
def get_monthly_transaction_summary(
    year: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user)
):
    """
    Get monthly transaction summary for the current user.
    """
    # This function would need to be implemented in the CRUD layer
    # and would typically involve a SQL query with GROUP BY.
    query = db.query(
        func.strftime("%Y-%m", Transaction.date).label("month"),
        func.sum(Transaction.amount).label("total_amount")
    ).filter(
        Transaction.user_id == current_user.id,
        func.strftime("%Y", Transaction.date) == str(year)
    ).group_by("month").all()
    return query