# Quick Start Guide

## Database Setup

### Using the Default Database
By default, the system uses `inventory.db`:
```bash
python -m uvicorn src.main:app --reload
```

### Using the Test/Demo Database
To use the pre-seeded test database with sample data:
```bash
INVENTORY_DB_URL=sqlite:///./inventory_test.db python -m uvicorn src.main:app --reload
```

### Creating a Fresh Test Database
To recreate the test database with seed data:
```bash
INVENTORY_DB_URL=sqlite:///./inventory_test.db python -m src.seed_test_data
```

## API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `POST /demo/login` - Quick demo user login/creation
- `GET /products/` - List all products
- `GET /products/{id}` - Get product details
- `POST /users/` - Create a new user
- `GET /users/{user_id}/cart` - Get user's cart
- `POST /users/{user_id}/cart` - Add item to cart
- `DELETE /users/{user_id}/cart/{item_id}` - Remove item from cart
- `POST /users/{user_id}/checkout` - Complete checkout
- `GET /users/{user_id}/orders` - Get user's order history
- `GET /users/{user_id}/orders/{order_id}` - Get specific order details

### Demo Login Example
```bash
curl -X POST http://localhost:8000/demo/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com"}'
```

### Get Products Example
```bash
curl http://localhost:8000/products/
```

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test File
```bash
python -m pytest tests/test_new_endpoints.py -v
```

### With Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Test Data

The seeded test database includes:
- 2 demo users (demo@example.com, student@example.com)
- 12 products across categories (Electronics, Accessories, Audio, Storage, Office, Bags)
- 2 shopping carts with items
- 2 completed orders with order history

## CORS Configuration

Frontend development servers are pre-configured:
- Vite: `http://localhost:5173`
- Create React App: `http://localhost:3000`

## Next Steps

To continue development:
1. Frontend setup (see `frontend-design.md`)
2. Additional API enhancements
3. Authentication system
4. Admin interface
