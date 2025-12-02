"""Tests for new API endpoints."""
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src.models import User, Product, Order, OrderItem

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_demo_login_new_user():
    """Test demo login creates new user."""
    response = client.post("/demo/login", json={"email": "newdemo@test.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "newdemo@test.com"
    assert "message" in data


def test_demo_login_existing_user():
    """Test demo login retrieves existing user."""
    # First login
    response1 = client.post("/demo/login", json={"email": "existing@test.com"})
    assert response1.status_code == 200
    user_id = response1.json()["user"]["id"]
    
    # Second login with same email
    response2 = client.post("/demo/login", json={"email": "existing@test.com"})
    assert response2.status_code == 200
    assert response2.json()["user"]["id"] == user_id


def test_get_product_details():
    """Test getting single product details."""
    # First get all products
    products_response = client.get("/products/")
    products = products_response.json()
    
    if products:
        product_id = products[0]["id"]
        
        # Get specific product
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == product_id
        assert "name" in product
        assert "price" in product


def test_get_product_not_found():
    """Test getting non-existent product returns 404."""
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_get_user_orders():
    """Test getting user order history."""
    # Create a user and complete checkout to generate an order
    user_response = client.post("/users/", json={"name": "Order User", "email": "orderuser@test.com"})
    user = user_response.json()
    user_id = user["id"]
    
    # Add item to cart
    products = client.get("/products/").json()
    if products:
        client.post(f"/users/{user_id}/cart", json={"product_id": products[0]["id"], "quantity": 1})
        
        # Checkout to create an order
        client.post(f"/users/{user_id}/checkout")
        
        # Get orders
        orders_response = client.get(f"/users/{user_id}/orders")
        assert orders_response.status_code == 200
        orders = orders_response.json()
        assert len(orders) >= 1
        assert orders[0]["user_id"] == user_id


def test_get_specific_order():
    """Test getting specific order details."""
    # Create user and order
    user_response = client.post("/users/", json={"name": "Order Detail User", "email": "orderdetail@test.com"})
    user = user_response.json()
    user_id = user["id"]
    
    products = client.get("/products/").json()
    if products:
        client.post(f"/users/{user_id}/cart", json={"product_id": products[0]["id"], "quantity": 2})
        checkout_response = client.post(f"/users/{user_id}/checkout")
        order_id = checkout_response.json()["order_id"]
        
        # Get specific order
        order_response = client.get(f"/users/{user_id}/orders/{order_id}")
        assert order_response.status_code == 200
        order = order_response.json()
        assert order["id"] == order_id
        assert order["user_id"] == user_id
        assert "items" in order
        assert len(order["items"]) == 1


def test_get_order_not_found():
    """Test getting non-existent order returns 404."""
    user_response = client.post("/users/", json={"name": "Test User", "email": "testorder@test.com"})
    user_id = user_response.json()["id"]
    
    response = client.get(f"/users/{user_id}/orders/99999")
    assert response.status_code == 404
