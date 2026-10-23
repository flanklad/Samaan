## Progress Update — FastAPI Testing

### What I learned

- **Pytest:** Runs automated tests and reports which tests pass or fail.
- **FastAPI TestClient:** Sends HTTP requests directly to the FastAPI application without needing to start the Uvicorn server.
- **Assertions:** `assert` verifies expected behavior. `response.status_code` checks the HTTP status, and `response.json()` reads the response body as a Python object.
- **Request validation:** FastAPI validates incoming request bodies against Pydantic schemas. A negative price or missing required field returns HTTP `422` when it violates the schema.
- **Fixtures:** Pytest fixtures provide reusable test setup and cleanup. My `reset_product_data` fixture clears the application's shared product list before and after relevant tests.

### Tests completed

- [x] Health endpoint returns HTTP 200 and the expected JSON.
- [x] Valid product creation returns HTTP 201 and the expected product fields.
- [x] Product creation with a negative price returns HTTP 422.
- [x] Product creation without the required name returns HTTP 422.

### Current limitations

- Product data is stored in an in-memory list and is lost when the application restarts.
- The test fixture resets the product list, but does not reset the global product ID counter.
- These tests cover selected behaviors, not every possible API scenario.

### Next steps

- Test `GET /products`, including category filtering and pagination.
- Expand validation and CRUD test coverage.
- Introduce PostgreSQL and a dedicated test database later.