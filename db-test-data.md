# Database & Test Data Design

This document describes the target database schema and how to create a seeded SQLite test database for demos and local testing.

---

## 1. Goals

- Have a **stable, deterministic test database** with realistic demo data.
- Keep the original dev database (if any) separate from demo/test data.
- Support workflows where instructors or students can reset the DB quickly.

---

## 2. Database Strategy

We maintain **two SQLite files** at the project root:

- `inventory.db` – original development DB (existing behavior).
- `inventory_test.db` – **demo/test DB** with seeded data.

The DB choice is controlled via an environment variable:

```bash
# Use test DB
export INVENTORY_DB_URL=sqlite:///./inventory_test.db

# Use original DB
export INVENTORY_DB_URL=sqlite:///./inventory.db
```

In `src/database.py`, we read this env var:

```python
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

---

## 3. Target Schema

> Note: Adjust names/types if the existing `models.py` differs. This is the intended logical design for the demo.

### 3.1 `users`

- `id` (PK, int)
- `email` (string, unique)
- `full_name` (string, nullable)
- `created_at` (datetime)

### 3.2 `products`

- `id` (PK, int)
- `name` (string)
- `sku` (string, unique)
- `description` (text)
- `price_cents` (int)
- `stock` (int)
- `image_url` (string, nullable) – for frontend card images
- `category` (string, nullable)
- `created_at` (datetime)

### 3.3 `carts`

- `id` (PK, int)
- `user_id` (FK → users.id, unique per user) – one active cart per user
- `created_at` (datetime)
- `updated_at` (datetime)

### 3.4 `cart_items`

- `id` (PK, int)
- `cart_id` (FK → carts.id)
- `product_id` (FK → products.id)
- `quantity` (int)

### 3.5 `orders`

- `id` (PK, int)
- `user_id` (FK → users.id)
- `total_cents` (int)
- `status` (string; e.g. `"completed"`, `"cancelled"`)
- `created_at` (datetime)

### 3.6 `order_items`

- `id` (PK, int)
- `order_id` (FK → orders.id)
- `product_id` (FK → products.id)
- `quantity` (int)
- `unit_price_cents` (int) – price at time of order

---

## 4. Test Data Seeding Script

We use a script `src/seed_test_data.py` to:

1. Drop all existing tables (optional but useful for clean resets).
2. Recreate tables via `Base.metadata.create_all(engine)`.
3. Insert:
   - Several **users** (including a main demo user).
   - A catalog of **products** in multiple categories.
   - At least one **cart** with items.
   - At least one **completed order** with order items.

### 4.1 Example Script Skeleton

```python
# src/seed_test_data.py
from datetime import datetime
from .database import SessionLocal, engine, Base
from . import models  # assumes models define User, Product, Cart, CartItem, Order, OrderItem

def seed():
    # Drop and recreate all tables (optional for demo)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # --- Users ---
    demo_user = models.User(
        email="demo@example.com",
        full_name="Demo User",
        created_at=datetime.utcnow(),
    )
    secondary_user = models.User(
        email="student@example.com",
        full_name="Student User",
        created_at=datetime.utcnow(),
    )

    db.add_all([demo_user, secondary_user])
    db.flush()  # get IDs

    # --- Products ---
    products = [
        models.Product(
            name="Wireless Mouse",
            sku="MOUSE-001",
            description="Compact wireless mouse with USB receiver.",
            price_cents=1999,
            stock=50,
            category="Accessories",
            created_at=datetime.utcnow(),
        ),
        models.Product(
            name="Mechanical Keyboard",
            sku="KEYBOARD-001",
            description="Mechanical keyboard with blue switches.",
            price_cents=5999,
            stock=30,
            category="Accessories",
            created_at=datetime.utcnow(),
        ),
        models.Product(
            name="27\" Monitor",
            sku="MONITOR-027",
            description="1080p IPS monitor suitable for office work and gaming.",
            price_cents=18999,
            stock=15,
            category="Displays",
            created_at=datetime.utcnow(),
        ),
        # Add ~10–15 products total across multiple categories
    ]
    db.add_all(products)
    db.flush()

    # --- Cart for demo user ---
    demo_cart = models.Cart(
        user_id=demo_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(demo_cart)
    db.flush()

    cart_items = [
        models.CartItem(
            cart_id=demo_cart.id,
            product_id=products[0].id,  # Wireless Mouse
            quantity=2,
        ),
        models.CartItem(
            cart_id=demo_cart.id,
            product_id=products[1].id,  # Mechanical Keyboard
            quantity=1,
        ),
    ]
    db.add_all(cart_items)

    # --- Completed order for demo user ---
    total_cents = (
        2 * products[0].price_cents +
        1 * products[1].price_cents
    )

    order = models.Order(
        user_id=demo_user.id,
        total_cents=total_cents,
        status="completed",
        created_at=datetime.utcnow(),
    )
    db.add(order)
    db.flush()

    order_items = [
        models.OrderItem(
            order_id=order.id,
            product_id=products[0].id,
            quantity=2,
            unit_price_cents=products[0].price_cents,
        ),
        models.OrderItem(
            order_id=order.id,
            product_id=products[1].id,
            quantity=1,
            unit_price_cents=products[1].price_cents,
        ),
    ]
    db.add_all(order_items)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
```

You can expand the product list and add more orders/carts as needed.

---

## 5. Creating / Resetting the Test Database

To (re)create `inventory_test.db`:

```bash
# Use the test DB URL and run the seed script
INVENTORY_DB_URL=sqlite:///./inventory_test.db python -m src.seed_test_data
```

This will:

- Drop all existing tables in `inventory_test.db`.
- Recreate the schema.
- Insert the demo users, products, carts, and orders.

---

## 6. Integration with Backend and Frontend

- Backend uses `INVENTORY_DB_URL` to connect to the correct DB
  (see [`backend-expansion.md`](./backend-expansion.md)).
- Frontend just calls the FastAPI API; it doesn’t talk to SQLite directly
  (see [`frontend-design.md`](./frontend-design.md)).

This separation makes it easy to adjust or swap out the database later if needed.
