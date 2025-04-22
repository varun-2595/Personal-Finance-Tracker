from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Transaction:
    db_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        category_id=transaction.category_id,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, transaction_id: int, user_id: int) -> Transaction:
    # Retrieve single transaction by ID
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

def get_user_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100, 
                          start_date: Optional[datetime] = None, end_date: Optional[datetime] = None,
                          category_id: Optional[int] = None) -> List[Transaction]:
    # Get list of transactions for a user with optional filters
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def update_transaction(db: Session, transaction_id: int, transaction: TransactionCreate) -> Transaction:
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.amount = transaction.amount
        db_transaction.description = transaction.description
        db_transaction.date = transaction.date
        db_transaction.category_id = transaction.category_id
        db_transaction.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int) -> bool:
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False