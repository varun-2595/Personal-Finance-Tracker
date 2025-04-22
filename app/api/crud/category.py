from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Category
from app.schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate, user_id: int) -> Category:
    db_category = Category(name=category.name, type=category.type, color=category.color, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int, user_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def get_user_categories(db: Session, user_id: int, type:Optional[str]=None) -> List[Category]:
    query = db.query(Category).filter(Category.user_id == user_id)
    if type:
        query = query.filter(Category.type == type)
    return query.all()

def update_category(db: Session, category_id: int, category_data: CategoryCreate, user_id: int,) -> Optional[Category]:
    db_category = get_category(db, category_id, user_id)
    if db_category:
        db_category.name = category_data.name
        db_category.type = category_data.type
        db_category.color = category_data.color
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    db_category = get_category(db, category_id, user_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False