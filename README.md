[![codecov](https://codecov.io/gh/Arian-D/comp684-demo/branch/main/graph/badge.svg)](https://app.codecov.io/gh/Arian-D/comp684-demo)  
  
comp684-demo — Inventory System MVP (demo)  
  
Overview  
--------  
An MVP implementation of an inventory system with users, shopping carts, cart items, and products. Built with FastAPI, SQLAlchemy, and SQLite for simplicity. Includes basic API endpoints for user management, product browsing, cart operations, and checkout.  
  
Features  
--------  
- User registration with automatic shopping cart creation  
- Product catalog with stock management  
- Shopping cart management (add/remove items)  
- Checkout with stock validation and automatic cart clearing  
- Seeded sample data for testing  
- Comprehensive test suite with API integration tests  
  
Run locally (Windows PowerShell)  
-------------------------------  
1. Create and activate a virtual environment:  
```powershell  
python -m venv venv  
.\venv\Scripts\Activate.ps1