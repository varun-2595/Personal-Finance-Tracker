from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.category import Category, CategoryCreate
from app.api.crud.category import create_category, get_category, get_user_categories, update_category, delete_category
from app.api.auth import get_current_active_user


router = APIRouter()

@router.post("/", response_model=Category, status_code=201)
def create_category_endpoint(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user),
):
    """
    Create a new category.
    """
    return create_category(db=db, category=category, user_id=current_user.id)

@router.get("/{category_id}", response_model=Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user),
):
    """
    Get a category by ID.
    """
    category = get_category(db=db, category_id=category_id, user_id=current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user),
):
    """
    Update a category by ID.
    """
    updated_category = update_category(db=db, category_id=category_id, category_data=category, user_id=current_user.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", response_model=dict)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_active_user),
):
    """
    Delete a category by ID.
    """
    success = delete_category(db=db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}