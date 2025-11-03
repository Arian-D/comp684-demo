import sys
sys.path.insert(0, 'src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User, Product, ShoppingCart, CartItem
import pytest

@pytest.fixture(scope="module")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(db):
    user = User(name="John Doe", email="john@example.com", password_hash="hash")
    db.add(user)
    db.commit()
    assert user.id is not None
    assert user.name == "John Doe"

def test_create_product(db):
    product = Product(name="Test Product", price=10.99, stock=100)
    db.add(product)
    db.commit()
    assert product.id is not None
    assert product.stock == 100

def test_cart_relationship(db):
    user = User(name="Jane Doe", email="jane@example.com", password_hash="hash")
    cart = ShoppingCart(user=user)
    db.add(user)
    db.add(cart)
    db.commit()
    assert user.cart == cart
    assert cart.user == user
