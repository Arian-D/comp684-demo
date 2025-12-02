# Technical Documentation

## comp684-demo

### Architecture Overview
The `comp684-demo` project is an MVP implementation of an inventory system designed to manage users, shopping carts, cart items, and products. The system is built using FastAPI for the backend, SQLAlchemy for ORM, and SQLite for simplicity. The architecture is modular and follows best practices for scalability and maintainability.

### Setup & Installation
To set up and run the project locally, follow these steps:

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```powershell
   uvicorn src.main:app --reload
   ```

### API Documentation
The API endpoints for the inventory system are as follows:

- **User Management:**
  - `POST /users/`: Create a new user.
  - `GET /users/{user_id}/cart`: Get the shopping cart for a user.

- **Product Management:**
  - `GET /products/`: Get all products.

- **Shopping Cart:**
  - `POST /cart/`: Add items to the cart.
  - `DELETE /cart/`: Remove items from the cart.

- **Checkout:**
  - `POST /checkout/`: Process the order.

### Database Schema
The database schema for the inventory system includes the following tables:

- **user**: Stores user information.
  - `id`: Integer, Primary Key
  - `name`: String
  - `email`: String, Unique
  - `password_hash`: String

- **shopping_cart**: Represents a user's shopping cart.
  - `id`: Integer, Primary Key
  - `user_id`: Integer, Foreign Key referencing `user.id`

- **cart_item**: Represents an item in a cart.
  - `id`: Integer, Primary Key
  - `cart_id`: Integer, Foreign Key referencing `shopping_cart.id`
  - `product_id`: Integer, Foreign Key referencing `product.id`
  - `quantity`: Integer

- **product**: Represents a product in the inventory.
  - `id`: Integer, Primary Key
  - `name`: String
  - `price`: Float
  - `stock`: Integer

### Configuration
The configuration for the project is managed through environment variables and a `requirements.txt` file. The `requirements.txt` file lists the dependencies required to run the project.

### Development Guidelines
- **Code Style**: Follow PEP 8 guidelines for Python code.
- **Testing**: Use `pytest` for unit and integration tests. Property-based testing is also used with `hypothesis`.
- **Version Control**: Use Git for version control and GitHub for remote repositories.

### Deployment Instructions
To deploy the project, follow these steps:

1. **Build Docker Image:**
   ```dockerfile
   FROM python:3.12

   WORKDIR /app

   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt

   COPY . .

   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Run Docker Container:**
   ```sh
   docker build -t comp684-demo .
   docker run -p 8000:8000 comp684-demo
   ```

3. **Kubernetes Deployment:**
   - Create a Kubernetes deployment YAML file.
   - Apply the deployment using `kubectl apply -f deployment.yaml`.

### Example Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: comp684-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: comp684-demo
  template:
    metadata:
      labels:
        app: comp684-demo
    spec:
      containers:
      - name: comp684-demo
        image: comp684-demo:latest
        ports:
        - containerPort: 8000
```

### Conclusion
The `comp684-demo` project provides a robust and scalable inventory system using modern Python frameworks and best practices. The modular architecture and comprehensive testing ensure reliability and maintainability.