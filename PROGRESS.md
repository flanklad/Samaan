# Samaan --- Project Progress

## Project Overview

Samaan is a learning project for building an inventory management API
with Python and FastAPI. The project is being developed incrementally,
with testing and Git practices learned alongside implementation.

**Current stage:** FastAPI and REST API fundamentals, with automated
tests for health checks and product endpoints.

## Environment and Tooling

-   Python 3.12
-   `uv` for project dependencies and environment management
-   FastAPI for HTTP API routes
-   Uvicorn for running the development server
-   Pydantic schemas for request validation and response data
-   Pytest and FastAPI `TestClient` for automated tests
-   Git for local version control
-   GitHub remote: `https://github.com/flanklad/Samaan.git`

## Implemented Application Features

-   `GET /health` --- returns a health status.
-   `GET /products` --- lists products.
-   `GET /products/{product_id}` --- retrieves a product by ID.
-   `POST /products` --- creates a product.
-   `PATCH /products/{product_id}` --- updates selected product fields.
-   `DELETE /products/{product_id}` --- deletes a product.
-   Product schemas are separated into `ProductCreate`,
    `ProductResponse`, and `ProductUpdate`.
-   Product routes are separated into `app/routers/products.py`.
-   Product data currently lives in an in-memory list in
    `app/products_data.py`.
-   The product-list endpoint supports category filtering and pagination
    using `skip` and `limit`.

## Testing Progress

### Concepts learned

-   Pytest discovers and runs test functions such as `test_health`.
-   FastAPI's `TestClient` sends HTTP requests directly to the
    application without starting Uvicorn.
-   `client.get(...)` and `client.post(...)` simulate HTTP requests.
-   The `json=` argument sends a dictionary as a JSON request body.
-   `response.status_code` checks the HTTP status code.
-   `response.json()` decodes the JSON response body into Python data
    structures.
-   `assert` checks that observed behavior matches the expected result.
-   FastAPI validates request bodies against Pydantic schemas and query
    parameters against declared constraints.
-   Invalid request data or invalid query parameters can produce HTTP
    `422`.
-   Pytest fixtures can provide setup and cleanup. The
    `reset_product_data` fixture clears the application's shared product
    list before and after relevant tests.
-   Tests should arrange their own data rather than depend on data left
    by other tests.
-   Category filtering should be tested with matching and non-matching
    products.
-   Pagination tests should use a known product order and verify both
    the number and identity/order of returned products.
-   Empty search results should return HTTP `200` with an empty list
    when the request itself is valid.

### Tests implemented

The following tests have been added during development:

-   [x] Health endpoint returns HTTP `200` and the expected JSON.
-   [x] Valid product creation returns HTTP `201` and the expected
    product fields.
-   [x] Product creation with a negative price returns HTTP `422`.
-   [x] Product creation without the required name returns HTTP `422`.
-   [x] Product listing returns the expected product data.
-   [x] Category filtering returns only products in the requested
    category.
-   [x] Pagination using `skip` and `limit` returns the expected
    products in order.
-   [x] A category with no matching products returns HTTP `200` and an
    empty list.
-   [x] Negative `skip` is rejected with HTTP `422`.
-   [x] A `limit` above the configured maximum is rejected with HTTP
    `422`.

**Expected suite size after the latest additions:** 10 tests. Run
`uv run pytest -v` to verify the current result before treating all
tests as passing.

### Known testing limitations

-   The fixture resets the shared `products` list but does not reset the
    global product ID counter.
-   Tests currently use the application's in-memory store rather than a
    dedicated test database.
-   The test suite covers selected behaviors, not every possible CRUD
    edge case.
-   The current store is global mutable state and is not suitable for
    concurrent or multi-process production use.

## Git and GitHub Progress

-   [x] Initialized a local Git repository in the Samaan project root.
-   [x] Created `.gitignore` to exclude the virtual environment,
    generated Python files, test cache, IDE settings, and environment
    secrets.
-   [x] Staged and reviewed the initial project files.
-   [x] Created the first commit:
    `e484e7f test: add product creation validation tests`.
-   [x] Configured the GitHub remote `origin` to point to
    `https://github.com/flanklad/Samaan.git`.
-   [x] The initial push was reported as completed by the user.
-   [ ] Commit the new list-endpoint tests and this progress update
    after running tests and reviewing the staged changes.
-   [ ] Verify the latest push and repository state after the next
    commit.

Useful commands learned:

``` powershell
git status
git diff
git add <files>
git diff --staged
git diff --staged --check
git commit -m "type: describe the change"
git log -1 --oneline
git push
```

## Current Limitations

-   Product data is stored in memory and is lost when the application
    restarts.
-   The product ID counter is global in-memory state and does not reset
    when the test fixture clears the product list.
-   Database persistence, authentication, authorization, and production
    deployment are not implemented.
-   PostgreSQL transactions and concurrency controls for inventory
    updates have not yet been implemented.

## Next Steps

1.  Run `uv run pytest -v` and verify the full test suite.
2.  Review and commit the product-list filtering, pagination, and
    validation tests.
3.  Continue testing the remaining product CRUD edge cases.
4.  Introduce PostgreSQL, SQLAlchemy, and Alembic migrations.
5.  Add a service layer and explicit business rules.
6.  Model warehouses, suppliers, purchase orders, inventory balances,
    and stock movements.
7.  Test inventory invariants, partial purchase-order receiving, and
    invalid stock transitions.
8.  Address concurrent stock updates, locking, and transaction
    boundaries.
9.  Add authentication, role-based access control, Docker, and
    deployment configuration.

## Working Principle

Documentation and test results should reflect what has actually been
implemented and verified. Update this file as the project changes; do
not mark planned work as complete until it has been built and tested.
