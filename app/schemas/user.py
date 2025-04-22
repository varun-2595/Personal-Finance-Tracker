from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    
class UserCreate(UserBase):
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: Optional[str] = None
    
class User(UserBase):
    id: int
    is_active: bool = Field(default=True, alias="isActive")
    
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dicts