from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    cart = relationship("ShoppingCart", uselist=False, back_populates="user")

class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

    def notify(self, message: str):
        """Log a notification message to the console."""
        print(message)

class CartItem(Base):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('shopping_cart.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product")

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
