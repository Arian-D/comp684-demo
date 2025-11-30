# Backend Expansion Plan (FastAPI)

This document describes how to expand the existing FastAPI backend into a full demo-ready API that supports a React frontend and a seeded test database.

---

## 1. Context and Goals

### 1.1 Current State

The current project is an inventory system MVP with:

- **FastAPI** as the web framework
- **SQLAlchemy** as ORM
- **SQLite** as the database (e.g. `inventory.db`)
- Core domain: **users**, **products**, **shopping carts**, **cart items**, basic **checkout**

Existing endpoints (simplified):

- `POST /users/` – Create user  
- `GET /products/` – List products  
- `GET /users/{user_id}/cart` – Get cart  
- `POST /users/{user_id}/cart` – Add to cart  
- `DELETE /users/{user_id}/cart/{item_id}` – Remove from cart  
- `POST /users/{user_id}/checkout` – Checkout  

### 1.2 Expansion Goals

Backend should:

1. Serve as a stable API for a React SPA.
2. Support a **test/demo database** (separate from any dev DB).
3. Provide endpoints for:
   - Demo login
   - Product details
   - Cart management
   - Checkout with order creation
   - (Optional) Order history

For schema and seeding details, see [`db-test-data.md`](./db-test-data.md).

---

## 2. Backend Architecture Overview

### 2.1 Logical Structure

- `src/main.py`  
  - FastAPI app, routers, CORS.
- `src/models.py`  
  - SQLAlchemy ORM models for `User`, `Product`, `Cart`, `CartItem`, `Order`, `OrderItem`, etc.
- `src/database.py`  
  - `engine`, `SessionLocal`, `Base`.
- `src/seed_test_data.py`  
  - Test data seeding script. (See [`db-test-data.md`](./db-test-data.md).)

### 2.2 Configuration via Environment

To support different SQLite files (dev vs test/demo), read a DB URL from an env var:

```python
# src/database.py (example)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("INVENTORY_DB_URL", "sqlite:///./inventory.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

- Default: `inventory.db`
- Demo: `inventory_test.db` via `INVENTORY_DB_URL=sqlite:///./inventory_test.db`

---

## 3. CORS and API Setup

### 3.1 CORS

The frontend (React) will run on a different port. Add CORS middleware:

```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # CRA default (optional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3.2 Health Check Endpoint

Add a simple health check for sanity and demos:

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## 4. Pydantic Schemas (Response Models)

Define response models so the frontend has predictable types. Example layout:

```python
# src/schemas.py (example)

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    id: int
    email: str
    full_name: Optional[str]

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id: int
    name: str
    sku: str
    description: str
    price_cents: int
    stock: int
    image_url: Optional[str]
    category: Optional[str]

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    id: int
    product: ProductBase
    quantity: int

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    id: int
    user_id: int
    items: List[CartItemBase]

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    id: int
    product: ProductBase
    quantity: int
    unit_price_cents: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id: int
    user_id: int
    total_cents: int
    status: str
    created_at: datetime
    items: List[OrderItemBase]

    class Config:
        orm_mode = True
```

You can add separate request models (`CreateUser`, `CreateCartItem`, etc.) as needed.

---

## 5. New / Refined Endpoints

### 5.1 Demo Login

A simple endpoint to bootstrap demo users.

**Endpoint:**

- `POST /demo/login`

**Request:**

```json
{
  "email": "demo@example.com"
}
```

**Behavior:**

- Look up user by `email`.
- If not found, create a new user with that email.
- Return user data (and optionally a simple demo token).

**Response:**

```json
{
  "user": {
    "id": 1,
    "email": "demo@example.com",
    "full_name": "Demo User"
  }
}
```

In the initial version, the frontend can just use `user.id` (no real auth).

---

### 5.2 Product List & Detail

**List:**

- `GET /products/`
- Response: list of `ProductBase` objects.

**Detail:**

- `GET /products/{product_id}`
- Response: single `ProductBase` with full description, etc.

The detail endpoint is used by the product detail page in the frontend.

---

### 5.3 Cart Management

Existing (or to be implemented/refined):

- `GET /users/{user_id}/cart`
  - Returns a `CartBase` with embedded items and their products.

- `POST /users/{user_id}/cart`
  - Request body: `{ "product_id": int, "quantity": int }`
  - Behavior:
    - If an item for that product already exists in the user’s cart, increase quantity.
    - Otherwise, create new `CartItem`.

- `DELETE /users/{user_id}/cart/{item_id}`
  - Removes an item from the cart.

Optional improvement: a dedicated endpoint to update quantity:

- `PATCH /users/{user_id}/cart/{item_id}`
  - Request: `{ "quantity": int }`

The frontend can use repeated `POST`s instead if this is not implemented.

---

### 5.4 Checkout and Order Creation

**Endpoint:**

- `POST /users/{user_id}/checkout`

**Expected behavior:**

1. Load the user’s cart and associated products.
2. Validate that each product has sufficient stock.
3. Deduct quantities from product stock.
4. Create an `Order` with:
   - `user_id`
   - `total_cents`
   - `status="completed"` (for demo)
   - `created_at`
5. For each cart item, create an `OrderItem` with:
   - `order_id`
   - `product_id`
   - `quantity`
   - `unit_price_cents` (price at time of checkout)
6. Clear the cart items.

**Response (example):**

```json
{
  "order": {
    "id": 42,
    "user_id": 1,
    "total_cents": 5997,
    "status": "completed",
    "created_at": "2025-01-01T12:00:00Z",
    "items": [
      {
        "id": 101,
        "product": { "id": 5, "name": "Wireless Mouse", "...": "..." },
        "quantity": 3,
        "unit_price_cents": 1999
      }
    ]
  }
}
```

The frontend will use `order.id` to show an order confirmation page.

---

### 5.5 Order History (Optional but Recommended)

To support an Order History page:

- `GET /users/{user_id}/orders`
  - Returns a list of `OrderBase` (without all item details or with truncated items).

- `GET /users/{user_id}/orders/{order_id}`
  - Returns a single `OrderBase` with full `items` list.

This allows the frontend to show:

- A table of past orders (`/orders` route).
- Detail page for a specific order (`/orders/:orderId`).

---

## 6. Local Backend Development

Steps to run the backend with the test database:

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .env\Scriptsctivate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the test database (see db-test-data.md)
INVENTORY_DB_URL=sqlite:///./inventory_test.db python -m src.seed_test_data

# 4. Run the API using the test DB
INVENTORY_DB_URL=sqlite:///./inventory_test.db uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

For frontend details, see [`frontend-design.md`](./frontend-design.md).
