from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- User ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

# --- Product ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True

# --- Order ---
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    pass

class OrderResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True