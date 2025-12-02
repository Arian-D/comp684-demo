#!/usr/bin/env python3
"""
Test data seeding script for the inventory system.
Creates a demo database with users, products, carts, and orders.

Usage:
    INVENTORY_DB_URL=sqlite:///./inventory_test.db python -m src.seed_test_data
"""
from datetime import datetime
from .database import SessionLocal, engine, Base
from . import models


def seed():
    """Seed the database with test data."""
    # Drop and recreate all tables for clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # --- Users ---
        demo_user = models.User(
            email="demo@example.com",
            name="Demo User",
            full_name="Demo User",
            password_hash="demo_hash_12345",
            created_at=datetime.utcnow(),
        )
        student_user = models.User(
            email="student@example.com",
            name="Student User",
            full_name="Student Test User",
            password_hash="student_hash_12345",
            created_at=datetime.utcnow(),
        )

        db.add_all([demo_user, student_user])
        db.flush()  # Get IDs

        # --- Products ---
        products = [
            # Electronics
            models.Product(
                name="Wireless Mouse",
                sku="MOUSE-001",
                description="Compact wireless mouse with USB receiver. Perfect for work and gaming.",
                price=19.99,
                price_cents=1999,
                stock=50,
                category="Accessories",
                image_url="/images/mouse.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Mechanical Keyboard",
                sku="KEYBOARD-001",
                description="Mechanical keyboard with blue switches. Tactile and clicky.",
                price=59.99,
                price_cents=5999,
                stock=30,
                category="Accessories",
                image_url="/images/keyboard.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name='27" Monitor',
                sku="MONITOR-027",
                description="1080p IPS monitor suitable for office work and gaming.",
                price=189.99,
                price_cents=18999,
                stock=15,
                category="Displays",
                image_url="/images/monitor.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="USB-C Hub",
                sku="HUB-001",
                description="7-in-1 USB-C hub with HDMI, USB 3.0, and card readers.",
                price=39.99,
                price_cents=3999,
                stock=75,
                category="Accessories",
                image_url="/images/usb-hub.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Laptop Stand",
                sku="STAND-001",
                description="Adjustable aluminum laptop stand for better ergonomics.",
                price=29.99,
                price_cents=2999,
                stock=40,
                category="Accessories",
                image_url="/images/laptop-stand.jpg",
                created_at=datetime.utcnow(),
            ),
            # More products
            models.Product(
                name="Webcam HD",
                sku="WEBCAM-001",
                description="1080p HD webcam with built-in microphone.",
                price=79.99,
                price_cents=7999,
                stock=25,
                category="Electronics",
                image_url="/images/webcam.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Headphones",
                sku="HEADPHONE-001",
                description="Noise-cancelling over-ear headphones with 30-hour battery.",
                price=149.99,
                price_cents=14999,
                stock=20,
                category="Audio",
                image_url="/images/headphones.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="External SSD 1TB",
                sku="SSD-1TB-001",
                description="Portable 1TB SSD with USB-C connection. Up to 1000MB/s.",
                price=119.99,
                price_cents=11999,
                stock=35,
                category="Storage",
                image_url="/images/ssd.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Desk Lamp LED",
                sku="LAMP-001",
                description="Adjustable LED desk lamp with touch controls and USB charging.",
                price=34.99,
                price_cents=3499,
                stock=60,
                category="Office",
                image_url="/images/lamp.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Cable Management Kit",
                sku="CABLE-001",
                description="Complete cable management solution with clips and sleeves.",
                price=15.99,
                price_cents=1599,
                stock=100,
                category="Accessories",
                image_url="/images/cables.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Laptop Backpack",
                sku="BACKPACK-001",
                description="Water-resistant laptop backpack with USB charging port.",
                price=49.99,
                price_cents=4999,
                stock=45,
                category="Bags",
                image_url="/images/backpack.jpg",
                created_at=datetime.utcnow(),
            ),
            models.Product(
                name="Wireless Charger",
                sku="CHARGER-001",
                description="Fast wireless charging pad compatible with Qi devices.",
                price=24.99,
                price_cents=2499,
                stock=80,
                category="Accessories",
                image_url="/images/charger.jpg",
                created_at=datetime.utcnow(),
            ),
        ]
        db.add_all(products)
        db.flush()

        # --- Cart for demo user ---
        demo_cart = models.ShoppingCart(
            user_id=demo_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(demo_cart)
        db.flush()

        cart_items = [
            models.CartItem(
                cart_id=demo_cart.id,
                product_id=products[0].id,  # Wireless Mouse
                quantity=2,
            ),
            models.CartItem(
                cart_id=demo_cart.id,
                product_id=products[1].id,  # Mechanical Keyboard
                quantity=1,
            ),
        ]
        db.add_all(cart_items)

        # --- Cart for student user ---
        student_cart = models.ShoppingCart(
            user_id=student_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(student_cart)
        db.flush()

        # --- Completed order for demo user ---
        order_total_cents = (2 * products[0].price_cents + 1 * products[1].price_cents)

        order = models.Order(
            user_id=demo_user.id,
            total_cents=order_total_cents,
            status="completed",
            created_at=datetime.utcnow(),
        )
        db.add(order)
        db.flush()

        order_items = [
            models.OrderItem(
                order_id=order.id,
                product_id=products[0].id,
                quantity=2,
                unit_price_cents=products[0].price_cents,
            ),
            models.OrderItem(
                order_id=order.id,
                product_id=products[1].id,
                quantity=1,
                unit_price_cents=products[1].price_cents,
            ),
        ]
        db.add_all(order_items)

        # --- Another order for student user ---
        order2_total_cents = products[2].price_cents

        order2 = models.Order(
            user_id=student_user.id,
            total_cents=order2_total_cents,
            status="completed",
            created_at=datetime.utcnow(),
        )
        db.add(order2)
        db.flush()

        order2_items = [
            models.OrderItem(
                order_id=order2.id,
                product_id=products[2].id,  # Monitor
                quantity=1,
                unit_price_cents=products[2].price_cents,
            ),
        ]
        db.add_all(order2_items)

        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created {len([demo_user, student_user])} users")
        print(f"   - Created {len(products)} products")
        print(f"   - Created 2 shopping carts with items")
        print(f"   - Created 2 completed orders")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
