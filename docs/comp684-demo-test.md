# Test Scenarios Document
## Project: comp684-demo

### 1. Test Strategy Overview
- **Testing Approach and Methodology**: We will use a combination of unit tests, integration tests, end-to-end tests, performance tests, and security tests. The primary testing framework will be pytest.
- **Test Scope and Objectives**: The goal is to ensure the functionality, performance, and security of the inventory system. We will test all major features, including user management, product catalog, shopping cart, and checkout.
- **Risk Assessment and Mitigation**: High-risk areas include user authentication, data integrity, and performance under load. We will prioritize these areas and implement thorough testing and monitoring.
- **Test Environment Requirements**: The test environment will include a local development setup with a SQLite database, a staging environment for integration and end-to-end tests, and a production-like environment for performance and security testing.

### 2. Functional Test Scenarios

#### Positive Test Cases
- **User Registration**: Verify that a new user can register successfully.
  - **Test ID**: FUNC-001
  - **Test Description**: Test user registration with valid input.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/users/` with valid user data.
    2. Verify the response status code is 200.
    3. Verify the response contains the user's name and email.
  - **Expected Results**: User is created successfully.
  - **Test Data**: `{"name": "Test User", "email": "test@example.com"}`
  - **Priority**: High

- **Product Browsing**: Verify that users can browse products.
  - **Test ID**: FUNC-002
  - **Test Description**: Test product browsing with valid input.
  - **Preconditions**: Products are seeded in the database.
  - **Test Steps**:
    1. Send a GET request to `/products/`.
    2. Verify the response status code is 200.
    3. Verify the response contains a list of products.
  - **Expected Results**: Products are listed successfully.
  - **Test Data**: None
  - **Priority**: High

#### Negative Test Cases
- **Invalid User Registration**: Verify that invalid user data is rejected.
  - **Test ID**: FUNC-003
  - **Test Description**: Test user registration with invalid input.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/users/` with invalid user data.
    2. Verify the response status code is 422.
    3. Verify the response contains an error message.
  - **Expected Results**: User registration fails with an error message.
  - **Test Data**: `{"name": "", "email": "invalid@example.com"}`
  - **Priority**: High

- **Non-existent Product**: Verify that a request for a non-existent product returns an error.
  - **Test ID**: FUNC-004
  - **Test Description**: Test product browsing with a non-existent product ID.
  - **Preconditions**: Products are seeded in the database.
  - **Test Steps**:
    1. Send a GET request to `/products/{non_existent_id}`.
    2. Verify the response status code is 404.
    3. Verify the response contains an error message.
  - **Expected Results**: Product not found error is returned.
  - **Test Data**: `non_existent_id`
  - **Priority**: Medium

#### Edge Cases
- **Empty Product List**: Verify that an empty product list is handled correctly.
  - **Test ID**: FUNC-005
  - **Test Description**: Test product browsing with an empty product list.
  - **Preconditions**: No products are seeded in the database.
  - **Test Steps**:
    1. Send a GET request to `/products/`.
    2. Verify the response status code is 200.
    3. Verify the response contains an empty list.
  - **Expected Results**: An empty product list is returned.
  - **Test Data**: None
  - **Priority**: Medium

### 3. Unit Test Scenarios

#### Function/Method Testing
- **User Model Creation**: Verify that a user can be created successfully.
  - **Test ID**: UNIT-001
  - **Test Description**: Test user model creation.
  - **Preconditions**: None
  - **Test Steps**:
    1. Create a new user object with valid data.
    2. Verify the user object has the correct attributes.
  - **Expected Results**: User object is created successfully.
  - **Test Data**: `{"name": "John Doe", "email": "john@example.com", "password_hash": "hash"}`
  - **Priority**: High

- **Product Model Creation**: Verify that a product can be created successfully.
  - **Test ID**: UNIT-002
  - **Test Description**: Test product model creation.
  - **Preconditions**: None
  - **Test Steps**:
    1. Create a new product object with valid data.
    2. Verify the product object has the correct attributes.
  - **Expected Results**: Product object is created successfully.
  - **Test Data**: `{"name": "Test Product", "price": 10.99, "stock": 100}`
  - **Priority**: High

#### Class/Component Testing
- **ShoppingCart Class**: Verify that the shopping cart class functions correctly.
  - **Test ID**: UNIT-003
  - **Test Description**: Test shopping cart class methods.
  - **Preconditions**: None
  - **Test Steps**:
    1. Create a new shopping cart object.
    2. Add items to the cart.
    3. Remove items from the cart.
    4. Calculate the total price of the cart.
  - **Expected Results**: Shopping cart operations are performed correctly.
  - **Test Data**: None
  - **Priority**: High

### 4. Integration Test Scenarios

#### API Integration
- **User Registration API**: Verify that the user registration API works correctly.
  - **Test ID**: INT-001
  - **Test Description**: Test user registration API integration.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/users/` with valid user data.
    2. Verify the response status code is 200.
    3. Verify the response contains the user's name and email.
  - **Expected Results**: User is created successfully.
  - **Test Data**: `{"name": "Test User", "email": "test@example.com"}`
  - **Priority**: High

- **Product Browsing API**: Verify that the product browsing API works correctly.
  - **Test ID**: INT-002
  - **Test Description**: Test product browsing API integration.
  - **Preconditions**: Products are seeded in the database.
  - **Test Steps**:
    1. Send a GET request to `/products/`.
    2. Verify the response status code is 200.
    3. Verify the response contains a list of products.
  - **Expected Results**: Products are listed successfully.
  - **Test Data**: None
  - **Priority**: High

#### Database Integration
- **User Creation**: Verify that user creation is persisted in the database.
  - **Test ID**: INT-003
  - **Test Description**: Test user creation database integration.
  - **Preconditions**: None
  - **Test Steps**:
    1. Create a new user object with valid data.
    2. Verify the user object is added to the database.
    3. Verify the user object has the correct attributes.
  - **Expected Results**: User is created and persisted in the database.
  - **Test Data**: `{"name": "John Doe", "email": "john@example.com", "password_hash": "hash"}`
  - **Priority**: High

### 5. End-to-End Test Scenarios

#### User Journey Testing
- **User Registration and Login**: Verify that a user can register and log in successfully.
  - **Test ID**: E2E-001
  - **Test Description**: Test user registration and login workflow.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/users/` with valid user data.
    2. Verify the response status code is 200.
    3. Verify the response contains the user's name and email.
    4. Send a POST request to `/login/` with valid user credentials.
    5. Verify the response status code is 200.
    6. Verify the response contains a JWT token.
  - **Expected Results**: User registers and logs in successfully.
  - **Test Data**: `{"name": "Test User", "email": "test@example.com"}`, `{"email": "test@example.com", "password": "password"}`
  - **Priority**: High

#### Cross-browser/Platform Testing
- **Product Browsing**: Verify that product browsing works across different browsers and platforms.
  - **Test ID**: E2E-002
  - **Test Description**: Test product browsing cross-browser compatibility.
  - **Preconditions**: Products are seeded in the database.
  - **Test Steps**:
    1. Send a GET request to `/products/` from different browsers and platforms.
    2. Verify the response status code is 200.
    3. Verify the response contains a list of products.
  - **Expected Results**: Product browsing works across different browsers and platforms.
  - **Test Data**: None
  - **Priority**: Medium

### 6. Performance Test Scenarios

#### Load Testing
- **User Registration**: Verify that the user registration API can handle multiple concurrent requests.
  - **Test ID**: PERF-001
  - **Test Description**: Test user registration load performance.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send multiple concurrent POST requests to `/users/` with valid user data.
    2. Measure the response time and throughput.
  - **Expected Results**: User registration API handles multiple concurrent requests.
  - **Test Data**: `{"name": "Test User", "email": "test@example.com"}`
  - **Priority**: High

#### Stress Testing
- **Product Browsing**: Verify that the product browsing API can handle peak traffic.
  - **Test ID**: PERF-002
  - **Test Description**: Test product browsing stress performance.
  - **Preconditions**: Products are seeded in the database.
  - **Test Steps**:
    1. Send multiple concurrent GET requests to `/products/`.
    2. Measure the response time and throughput.
  - **Expected Results**: Product browsing API handles peak traffic.
  - **Test Data**: None
  - **Priority**: High

### 7. Security Test Scenarios

#### Authentication Testing
- **User Login**: Verify that user login is secure and returns a valid JWT token.
  - **Test ID**: SEC-001
  - **Test Description**: Test user login security.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/login/` with valid user credentials.
    2. Verify the response status code is 200.
    3. Verify the response contains a JWT token.
  - **Expected Results**: User logs in successfully and receives a JWT token.
  - **Test Data**: `{"email": "test@example.com", "password": "password"}`
  - **Priority**: High

#### Authorization Testing
- **Admin Product Management**: Verify that only admin users can manage products.
  - **Test ID**: SEC-002
  - **Test Description**: Test admin product management authorization.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/products/` with valid product data and admin credentials.
    2. Verify the response status code is 200.
    3. Verify the response contains the product data.
    4. Send a POST request to `/products/` with valid product data and non-admin credentials.
    5. Verify the response status code is 403.
    6. Verify the response contains an error message.
  - **Expected Results**: Admin users can manage products, non-admin users cannot.
  - **Test Data**: `{"name": "Test Product", "price": 10.99, "stock": 100}`, `{"email": "admin@example.com", "password": "admin"}`, `{"email": "user@example.com", "password": "user"}`
  - **Priority**: High

### 8. Error Handling & Recovery Test Scenarios

#### Exception Handling
- **User Registration Error**: Verify that user registration errors are handled gracefully.
  - **Test ID**: ERR-001
  - **Test Description**: Test user registration error handling.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a POST request to `/users/` with invalid user data.
    2. Verify the response status code is 422.
    3. Verify the response contains an error message.
  - **Expected Results**: User registration error is handled gracefully.
  - **Test Data**: `{"name": "", "email": "invalid@example.com"}`
  - **Priority**: High

#### Fallback Mechanisms
- **Product Browsing Error**: Verify that product browsing errors are handled gracefully.
  - **Test ID**: ERR-002
  - **Test Description**: Test product browsing error handling.
  - **Preconditions**: None
  - **Test Steps**:
    1. Send a GET request to `/products/{non_existent_id}`.
    2. Verify the response status code is 404.
    3. Verify the response contains an error message.
  - **Expected Results**: Product browsing error is handled gracefully.
  - **Test Data**: `non_existent_id`
  - **Priority**: Medium

### 9. Test Data Requirements

#### Test Data Sets
- **User Data**: Valid and invalid user data for registration and login.
  - **Test Data**: `{"name": "Test User", "email": "test@example.com"}`, `{"name": "", "email": "invalid@example.com"}`

- **Product Data**: Valid and invalid product data for browsing and management.
  - **Test Data**: `{"name": "Test Product", "price": 10.99, "stock": 100}`, `{"name": "", "price": -10.99, "stock": -100}`

#### Data Setup/Teardown
- **Test Environment Setup**: Create and seed the database with initial data.
  - **Test Steps**:
    1. Create a new SQLite database.
    2. Seed the database with initial data.
  - **Expected Results**: Database is created and seeded successfully.
  - **Test Data**: None

- **Test Environment Teardown**: Drop the database after tests are complete.
  - **Test Steps**:
    1. Drop the database.
  - **Expected Results**: Database is dropped successfully.
  - **Test Data**: None

### 10. Test Automation Recommendations

#### Automation Strategy
- **Automate Unit Tests**: Automate all unit tests to ensure code quality and reliability.
- **Automate Integration Tests**: Automate integration tests to ensure API and database interactions are working correctly.
- **Automate End-to-End Tests**: Automate end-to-end tests to ensure the complete user workflow is working correctly.
- **Automate Performance Tests**: Automate performance tests to ensure the system can handle expected traffic and peak loads.
- **Automate Security Tests**: Automate security tests to ensure the system is secure and compliant with best practices.

#### Test Framework Suggestions
- **pytest**: Recommended for unit, integration, and end-to-end tests.
- **pytest-cov**: Recommended for code coverage analysis.
- **locust**: Recommended for performance testing.
- **OWASP ZAP**: Recommended for security testing.

#### CI/CD Integration
- **Automated Testing Pipeline**: Integrate automated tests into the CI/CD pipeline to ensure tests are run on every code change.
  - **Test Steps**:
    1. Trigger tests on code commit.
    2. Run tests and collect results.
    3. Fail the build if tests fail.
  - **Expected Results**: Tests are run automatically and build fails if tests fail.
  - **Test Data**: None

#### Maintenance Guidelines
- **Keep Tests Updated**: Regularly update tests to reflect changes in the codebase.
- **Review Test Coverage**: Regularly review test coverage to ensure critical paths are tested.
- **Refactor Tests**: Refactor tests to improve maintainability and readability.

### 11. Acceptance Criteria & Test Cases

#### Given-When-Then Scenarios
- **User Registration**:
  - **Given**: A user wants to register.
  - **When**: The user submits a registration form with valid data.
  - **Then**: The user is registered successfully and receives a confirmation message.

- **Product Browsing**:
  - **Given**: A user wants to browse products.
  - **When**: The user accesses the product browsing page.
  - **Then**: The user sees a list of products.

#### Test Case Templates
- **Test Case ID**: FUNC-001
- **Test Case Description**: Test user registration with valid input.
- **Test Steps**:
  1. Send a POST request to `/users/` with valid user data.
  2. Verify the response status code is 200.
  3. Verify the response contains the user's name and email.
- **Expected Results**: User is created successfully.
- **Test Data**: `{"name": "Test User", "email": "test@example.com"}`
- **Priority**: High

#### Traceability Matrix
| Requirement ID | Test Case ID | Test Description |
|----------------|--------------|------------------|
| REQ-001        | FUNC-001     | User registration with valid input |
| REQ-002        | FUNC-002     | Product browsing with valid input |
| REQ-003        | FUNC-003     | User registration with invalid input |
| REQ-004        | FUNC-004     | Product browsing with non-existent product ID |
| REQ-005        | FUNC-005     | Product browsing with empty product list |

### 12. Risk-Based Testing

#### High-Risk Areas
- **User Authentication**: Critical functionality that needs thorough testing.
  - **Test ID**: SEC-001
  - **Test Description**: Test user login security.
  - **Priority**: High

- **Data Integrity**: Ensuring data consistency and integrity during error conditions.
  - **Test ID**: ERR-001
  - **Test Description**: Test user registration error handling.
  - **Priority**: High

#### Medium-Risk Areas
- **Product Management**: Important feature with moderate testing needs.
  - **Test ID**: FUNC-002
  - **Test Description**: Test product browsing with valid input.
  - **Priority**: Medium

#### Low-Risk Areas
- **Empty Product List**: Basic functionality with minimal testing requirements.
  - **Test ID**: FUNC-005
  - **Test Description**: Test product browsing with an empty product list.
  - **Priority**: Low

For each test scenario, include:
- **Test ID**: Unique identifier
- **Test Description**: Clear description of what is being tested
- **Preconditions**: Required setup before test execution
- **Test Steps**: Detailed steps to execute the test
- **Expected Results**: What should happen when test passes
- **Test Data**: Required input data and conditions
- **Priority**: High/Medium/Low based on risk and impact