class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id: str, quantity: int, price: float):
        """Add an item to the shopping cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        if item_id in self.items:
            self.items[item_id]["quantity"] += quantity
        else:
            self.items[item_id] = {
                "quantity": quantity,
                "price": price
            }

    def remove_item(self, item_id: str, quantity: int = None):
        """Remove an item from the shopping cart."""
        if item_id not in self.items:
            raise ValueError("Item not in cart")
        
        if quantity is None or quantity >= self.items[item_id]["quantity"]:
            del self.items[item_id]
        else:
            self.items[item_id]["quantity"] -= quantity

    def get_total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(
            item["quantity"] * item["price"]
            for item in self.items.values()
        )

    def notify(self, message: str):
        """Log a notification message to the console."""
        print(message)