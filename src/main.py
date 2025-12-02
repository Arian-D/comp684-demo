from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, engine
from .models import Base, User, Product, ShoppingCart, CartItem, Order, OrderItem
from . import schemas
from contextlib import asynccontextmanager
import uvicorn

# ✅ Ensure tables exist before app runs (important for tests)
Base.metadata.create_all(bind=engine)


# ✅ Add a schema for JSON user creation (fixes 422 Unprocessable Entity)
class UserCreate(BaseModel):
    name: str
    email: str

class AddToCart(BaseModel):
    product_id: int
    quantity: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup and shutdown."""
    db = SessionLocal()
    # Seed products if DB empty
    if not db.query(Product).first():
        products = [
            Product(name="Laptop", price=999.99, price_cents=99999, stock=10, sku="LAP-001", category="Electronics"),
            Product(name="Mouse", price=25.99, price_cents=2599, stock=50, sku="MOUSE-001", category="Accessories"),
            Product(name="Keyboard", price=75.99, price_cents=7599, stock=30, sku="KEY-001", category="Accessories"),
        ]
        db.add_all(products)
        db.commit()
    db.close()
    yield
    # Shutdown logic (if needed)


app = FastAPI(lifespan=lifespan)

# CORS middleware for frontend support
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # CRA default
        "http://localhost:5500",  # Local development
        "https://fluffy-space-halibut-5jqj9rwrwvg2vj44-5500.app.github.dev",  # Codespace frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Inventory System API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "demo_login": "/demo/login",
            "products": "/products/",
            "cart": "/users/{user_id}/cart",
            "checkout": "/users/{user_id}/checkout",
            "orders": "/users/{user_id}/orders"
        }
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Demo login endpoint
@app.post("/demo/login", response_model=schemas.DemoLoginResponse)
def demo_login(request: schemas.DemoLoginRequest, db: Session = Depends(get_db)):
    """Create or retrieve a demo user for testing."""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Create new demo user
        user = User(
            name=request.email.split('@')[0],
            email=request.email,
            full_name=f"Demo {request.email.split('@')[0]}",
            password_hash="demo_hash"
        )
        # Create cart for user
        cart = ShoppingCart(user=user)
        db.add(user)
        db.add(cart)
        db.commit()
        db.refresh(user)
        message = "New demo user created"
    else:
        message = "Demo user retrieved"
    
    return schemas.DemoLoginResponse(
        user=schemas.UserBase.from_orm(user),
        message=message
    )


# ✅ Accept JSON body for user creation
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_obj = User(name=user.name, email=user.email, password_hash="dummy")  # Hash passwords in real apps
    cart = ShoppingCart(user=user_obj)
    db.add(user_obj)
    db.add(cart)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@app.get("/products/", response_model=list[schemas.ProductBase])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}", response_model=schemas.ProductBase)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get details for a specific product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/users/{user_id}/cart")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.items


@app.post("/users/{user_id}/cart")
def add_to_cart(user_id: int, payload: AddToCart, db: Session = Depends(get_db)):
    # ✅ Extract values from the JSON payload
    product_id = payload.product_id
    quantity = payload.quantity

    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.stock < quantity:
        raise HTTPException(status_code=400, detail="Product not available")

    # ✅ Create the cart item
    item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/users/{user_id}/cart/{item_id}")
def remove_from_cart(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item removed"}


@app.post("/users/{user_id}/checkout")
def checkout(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Calculate total and validate stock
    total = 0
    total_cents = 0
    for item in cart.items:
        if item.product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        total += item.quantity * item.product.price
        # Use price_cents if available, otherwise convert price
        price_cents = item.product.price_cents if item.product.price_cents else int(item.product.price * 100)
        total_cents += item.quantity * price_cents
    
    # Create order
    order = Order(
        user_id=user_id,
        total_cents=total_cents,
        status="completed"
    )
    db.add(order)
    db.flush()  # Get order ID
    
    # Create order items and update stock
    for item in cart.items:
        price_cents = item.product.price_cents if item.product.price_cents else int(item.product.price * 100)
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price_cents=price_cents
        )
        db.add(order_item)
        item.product.stock -= item.quantity
    
    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(order)
    
    return {
        "message": "Checkout successful",
        "total": total,
        "order_id": order.id,
        "total_cents": total_cents
    }


@app.get("/users/{user_id}/orders", response_model=list[schemas.OrderBase])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Get all orders for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


@app.get("/users/{user_id}/orders/{order_id}", response_model=schemas.OrderBase)
def get_order(user_id: int, order_id: int, db: Session = Depends(get_db)):
    """Get details for a specific order."""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
