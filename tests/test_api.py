import sys
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app, get_db
from src.models import Base, Product
import pytest

# TestClient will be created after the test DB is configured in the fixture
client = None

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Use a shared in-memory SQLite database so tables are visible across connections
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables in the shared in-memory DB
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Override dependency to use the test SessionLocal
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Seed products (the app's startup seeding won't run against this test DB)
    db = SessionLocal()
    try:
        if not db.query(Product).first():
            db.add_all([
                Product(name="Laptop", price=999.99, stock=10),
                Product(name="Mouse", price=25.99, stock=50),
                Product(name="Keyboard", price=75.99, stock=30),
            ])
            db.commit()
    finally:
        db.close()

    # Create TestClient after dependency overrides and DB setup
    global client
    client = TestClient(app)

    yield

    # Teardown: close TestClient and clear overrides
    client.close()
    app.dependency_overrides.pop(get_db, None)

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
    assert response.status_code == 200
    user_id = response.json()["id"]
    # Get an existing product id instead of assuming 1
    products_resp = client.get("/products/")
    assert products_resp.status_code == 200
    products = products_resp.json()
    assert len(products) > 0
    product_id = products[0]["id"]
    response = client.post(f"/users/{user_id}/cart", json={"product_id": product_id, "quantity": 1})
    assert response.status_code == 200
