from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    id: int
    email: str
    name: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    id: int
    name: str
    sku: Optional[str] = None
    description: Optional[str] = None
    price: float
    price_cents: Optional[int] = None
    stock: int
    image_url: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    id: int
    product: ProductBase
    quantity: int

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    id: int
    user_id: int
    items: List[CartItemBase]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    id: int
    product: ProductBase
    quantity: int
    unit_price_cents: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    id: int
    user_id: int
    total_cents: int
    status: str
    created_at: datetime
    items: List[OrderItemBase]

    class Config:
        from_attributes = True


class DemoLoginRequest(BaseModel):
    email: Optional[str] = "demo@example.com"


class DemoLoginResponse(BaseModel):
    user: UserBase
    message: str
