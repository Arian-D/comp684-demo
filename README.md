comp684-demo — Inventory System MVP (demo)

Overview
--------
An MVP implementation of an inventory system with users, shopping carts, cart items, and products. Built with FastAPI, SQLAlchemy, and SQLite for simplicity. Includes basic API endpoints for user management, product browsing, cart operations, and checkout.

Features
--------
- User registration
- Product catalog
- Shopping cart management (add/remove items)
- Checkout with stock validation
- Seeded sample data

Run locally (Windows PowerShell)
-------------------------------
1. Create and activate a virtual environment (if you don't already have one):

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the API server:

```powershell
python src/main.py
```

4. Run tests:

```powershell
python -m pytest -v
```

API Endpoints
-------------
- POST /users/ - Create user
- GET /products/ - List products
- GET /users/{user_id}/cart - Get cart
- POST /users/{user_id}/cart - Add to cart
- DELETE /users/{user_id}/cart/{item_id} - Remove from cart
- POST /users/{user_id}/checkout - Checkout

What I pushed
-------------
- `src/models.py` — SQLAlchemy models
- `src/database.py` — Database setup
- `src/main.py` — FastAPI app with endpoints
- `src/shopping_cart.py` — Original in-memory cart (kept for reference)
- `tests/test_models.py` — Model tests
- `tests/test_api.py` — API tests
- `tests/test_shopping_cart.py` — Original cart tests
- `design.md` — Requirements and implementation guide
- `AGENTS.md` — Design document
- `requirements.txt` — Dependencies
- `README.md` — this file

Next suggested improvements
-------------------------
- Add authentication and authorization
- Implement proper password hashing
- Add more validation and error handling
- Create a frontend (React)
- Add order history
- Deploy to cloud

Repository remote: https://github.com/Arian-D/comp684-demo
