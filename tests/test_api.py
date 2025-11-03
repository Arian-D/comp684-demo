import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.models import Base
import pytest

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.dependency_overrides[get_db] = lambda: SessionLocal()

def test_create_user():
    response = client.post("/users/", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Assuming seeded

def test_add_to_cart():
    # First create user
    response = client.post("/users/", json={"name": "Cart User", "email": "cart@example.com"})
    user_id = response.json()["id"]
    # Assume product id 1 exists
    response = client.post(f"/users/{user_id}/cart", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 200
