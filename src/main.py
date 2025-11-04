from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, User, Product, ShoppingCart, CartItem
from contextlib import asynccontextmanager
import uvicorn

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = SessionLocal()
    # Seed products
    if not db.query(Product).first():
        products = [
            Product(name="Laptop", price=999.99, stock=10),
            Product(name="Mouse", price=25.99, stock=50),
            Product(name="Keyboard", price=75.99, stock=30),
        ]
        db.add_all(products)
        db.commit()
    db.close()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email, password_hash="dummy")  # In real app, hash password
    cart = ShoppingCart(user=user)
    db.add(user)
    db.add(cart)
    db.commit()
    db.refresh(user)
    return user

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/users/{user_id}/cart")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart.items

@app.post("/users/{user_id}/cart")
def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.stock < quantity:
        raise HTTPException(status_code=400, detail="Product not available")
    item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
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
    total = 0
    for item in cart.items:
        if item.product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        total += item.quantity * item.product.price
        item.product.stock -= item.quantity
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"message": "Checkout successful", "total": total}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
