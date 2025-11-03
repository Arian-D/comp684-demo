from hypothesis import given, strategies as st
from src.shopping_cart import ShoppingCart
import pytest


@given(
    price=st.floats(min_value=0.01, max_value=100, allow_infinity=False, allow_nan=False),
    qty=st.integers(min_value=1, max_value=10)
)
def test_total_matches_price_times_quantity(price, qty):
    """Property-based test:
    The total should always equal price * quantity for valid inputs."""
    cart = ShoppingCart()
    cart.add_item("item", qty, price)  # ✅ correct argument order
    total = cart.get_total()
    assert pytest.approx(total) == price * qty


@given(
    qty=st.integers(min_value=-10, max_value=0),
    price=st.floats(min_value=-100, max_value=100, allow_infinity=False, allow_nan=False)
)
def test_invalid_add_item_raises(qty, price):
    """Invalid prices or quantities should raise ValueError."""
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item("item", qty, price)  # ✅ correct argument order
