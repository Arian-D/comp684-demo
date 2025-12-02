# comp684-demo

## 🚀 Overview
comp684-demo is an MVP implementation of an inventory system designed for an online store. This project leverages FastAPI for high-performance APIs, SQLAlchemy for ORM, and SQLite for simplicity. It includes essential features such as user registration, product browsing, shopping cart management, and checkout. The system is built with a focus on scalability, security, and ease of use.

## ✨ Features
- 👤 **User Registration**: Users can register with automatic shopping cart creation.
- 🛍️ **Product Catalog**: Browse and search products with stock management.
- 🛒 **Shopping Cart**: Add, remove, and view items in the shopping cart.
- 💳 **Checkout**: Process orders with stock validation and automatic cart clearing.
- 📊 **Seeded Sample Data**: Includes sample data for testing.
- 🔬 **Comprehensive Test Suite**: API integration tests for robust validation.

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Frameworks**: FastAPI, SQLAlchemy
- **Database**: SQLite
- **Testing**: Pytest, Hypothesis
- **Version Control**: Git

## 📦 Installation

### Prerequisites
- Python 3.12 or later
- Git

### Quick Start
```bash
# Step-by-step installation commands
git clone https://github.com/Arian-D/comp684-demo.git
cd comp684-demo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Alternative Installation Methods
- **Docker**: Use the provided Dockerfile to containerize the application.
- **Development Setup**: Follow the instructions in the `AGENTS.md` and `design.md` files for a more detailed setup.

## 🎯 Usage

### Basic Usage
```python
# Example of creating a user
response = client.post("/users/", json={"name": "Test User", "email": "test@example.com"})
print(response.json())
```

### Advanced Usage
- **Adding Items to Cart**:
  ```python
  response = client.post("/users/1/cart", json={"product_id": 1, "quantity": 2})
  print(response.json())
  ```

- **Removing Items from Cart**:
  ```python
  response = client.delete("/users/1/cart/1")
  print(response.json())
  ```

## 📁 Project Structure
```
comp684-demo/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── shopping_cart.py
│   └── database.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_hypothesis_cart.py
│   ├── test_models.py
│   └── test_shopping_cart.py
│
├── requirements.txt
├── AGENTS.md
├── design.md
├── test_report.txt
├── .github/
│   └── workflows/
│       └── test.yml
└── README.md
```

## 🔧 Configuration
- **Environment Variables**: Set any required environment variables in a `.env` file.
- **Configuration Files**: Refer to the `AGENTS.md` and `design.md` files for detailed configuration options.

## 🤝 Contributing
- Fork the repository
- Create a new branch (`git checkout -b feature/your-feature`)
- Commit your changes (`git commit -am 'Add some feature'`)
- Push to the branch (`git push origin feature/your-feature`)
- Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors & Contributors
- **Arian-D**: Initial development and project setup
- **Contributors**: [List of contributors]

## 🐛 Issues & Support
- Report issues on the [GitHub Issues page](https://github.com/Arian-D/comp684-demo/issues)
- For support, please open an issue or contact the maintainers.

## 🗺️ Roadmap
- **Planned Features**:
  - Implement user authentication
  - Add admin panel for product management
  - Enhance shopping cart UI/UX
- **Known Issues**:
  - [Issue #1](https://github.com/Arian-D/comp684-demo/issues/1)
- **Future Improvements**:
  - Integrate with a frontend framework
  - Add more comprehensive error handling

---

**Additional Guidelines:**
- Use modern markdown features (badges, collapsible sections, etc.)
- Include practical, working code examples
- Make it visually appealing with appropriate emojis
- Ensure all code snippets are syntactically correct for Python
- Include relevant badges (build status, version, license, etc.)
- Make installation instructions copy-pasteable
- Focus on clarity and developer experience