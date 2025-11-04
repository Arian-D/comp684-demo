import pytest
from src.shopping_cart import ShoppingCart

def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 1.0)
    assert "apple" in cart.items
    assert cart.items["apple"]["quantity"] == 2
    assert cart.items["apple"]["price"] == 1.0

def test_add_negative_quantity():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item("apple", -1, 1.0)

def test_add_negative_price():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.add_item("apple", 1, -1.0)

def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 1.0)
    cart.remove_item("apple")
    assert "apple" not in cart.items

def test_remove_partial_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 3, 1.0)
    cart.remove_item("apple", 2)
    assert cart.items["apple"]["quantity"] == 1

def test_remove_nonexistent_item():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.remove_item("apple")

def test_get_total():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 1.0)
    cart.add_item("banana", 3, 0.5)
    assert cart.get_total() == 3.5  # (2 * 1.0) + (3 * 0.5)

def test_notify(capsys):
    cart = ShoppingCart()
    cart.notify("Test message")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Test message"