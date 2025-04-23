from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base


class TimeStampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    

class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    financial_goals = relationship("FinancialGoal", back_populates="user", cascade="all, delete-orphan")
    

class Category(Base, TimeStampMixin):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    color = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name="check_category_type"),
    )
    
    # Relationships
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
    
    
class Transaction(Base, TimeStampMixin):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    

class Budget(Base, TimeStampMixin):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("period IN ('daily', 'weekly', 'monthly', 'yearly')", name="check_budget_period"),
    )
    
    # Relationships
    category = relationship("Category", back_populates="budgets")
    user = relationship("User", back_populates="budgets")
    

class FinancialGoal(Base, TimeStampMixin):
    __tablename__ = "financial_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    target_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, default=0.0, nullable=False)
    target_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="financial_goals")
    