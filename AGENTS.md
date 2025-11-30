# Inventory System Design Document  
  
## Overview  
This document outlines the design for an inventory system that includes users, shopping carts, cart items, and product inventory for an online store. The implementation uses FastAPI with SQLAlchemy ORM and SQLite database.  
  
## Entities and Relationships  
  
### Entities  
- **User**: Represents a store customer with personal information (id, name, email, password_hash)  
- **ShoppingCart**: Represents a user's shopping cart containing items (id, user_id)  
- **CartItem**: Represents an item in a cart with quantity (id, cart_id, product_id, quantity)  
- **Product**: Represents a product in the inventory with stock and pricing (id, name, price, stock)  
  
### Relationships  
- User has one ShoppingCart (1:1) - automatically created on user registration  
- ShoppingCart contains multiple CartItems (1:many) - items belong to a specific cart  
- CartItem references one Product (many:1) - each item points to a product  
  
## UML Class Diagram  
  
```mermaid  
classDiagram  
    class BaseModel {  
        +id: int  
    }  
      
    class User {  
        +name: str  
        +email: str  
        +password_hash: str  
        +cart: ShoppingCart  
    }  
      
    class ShoppingCart {  
        +user_id: int  
        +items: list[CartItem]  
    }  
      
    class CartItem {  
        +cart_id: int  
        +product_id: int  
        +quantity: int  
        +product: Product  
    }  
      
    class Product {  
        +name: str  
        +price: float  
        +stock: int  
    }  
      
    BaseModel <|-- User  
    BaseModel <|-- ShoppingCart  
    BaseModel <|-- CartItem  
    BaseModel <|-- Product  
      
    User ||--o{ ShoppingCart : has  
    ShoppingCart ||--o{ CartItem : contains  
    CartItem ||--|| Product : references