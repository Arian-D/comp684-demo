import pytest
from src.database import Base, engine, SessionLocal
from src.models import Product, User, ShoppingCart

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables and seed initial data before any tests run."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Open a session for seeding data
    db = SessionLocal()

    # ✅ Seed a product so /products and add_to_cart tests work
    if not db.query(Product).first():
        product = Product(name="Seeded Product", price=9.99, stock=20)
        db.add(product)

    # ✅ Seed a default user + cart if tests expect them
    if not db.query(User).first():
        user = User(name="Seeded User", email="seed@example.com", password_hash="dummy")
        db.add(user)
        db.flush()  # get user.id before creating cart
        cart = ShoppingCart(user_id=user.id)
        db.add(cart)

    db.commit()
    db.close()

    # Yield control to the tests
    yield

    # Drop tables after all tests (optional cleanup)
    Base.metadata.drop_all(bind=engine)
