import pytest
from src.database import Base, engine
from src.models import Product, User, ShoppingCart, CartItem

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables once before running any tests."""
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop tables after tests
    Base.metadata.drop_all(bind=engine)
