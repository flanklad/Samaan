[README.md](https://github.com/user-attachments/files/33888570/README.md)
# Samaan --- Inventory Management System

Samaan is a learning project for building an inventory management API
with Python and FastAPI. The goal is to grow it into a reliable
inventory management system with product, warehouse, supplier,
purchase-order, and stock-movement workflows.

> **Current status:** Early development. The current application uses
> in-memory storage; PostgreSQL persistence, authentication, and the
> wider inventory workflows are planned, not implemented yet.

## Current Features

-   Health-check endpoint: `GET /health`
-   Product creation: `POST /products`
-   Retrieve products: `GET /products`
-   Retrieve a product by ID: `GET /products/{product_id}`
-   Update a product: `PATCH /products/{product_id}`
-   Delete a product: `DELETE /products/{product_id}`
-   Product request validation using Pydantic schemas
-   Product-list category filtering and pagination
-   Automated tests using Pytest and FastAPI's `TestClient`

## Technology Stack

-   Python 3.12
-   FastAPI
-   Uvicorn
-   Pydantic
-   Pytest
-   HTTPX / Starlette test client
-   `uv` for dependency and environment management
-   Git and GitHub

PostgreSQL, SQLAlchemy, Alembic, Docker, and AWS are planned for later
stages.

## Getting Started

### Prerequisites

-   Python 3.12
-   `uv` installed and available on your PATH
-   Git

### Install dependencies

Clone the repository and enter the project directory:

``` powershell
git clone https://github.com/flanklad/Samaan.git
cd Samaan
```

Install the project dependencies from the project configuration and
lockfile:

``` powershell
uv sync
```

### Run the API

From the project root:

``` powershell
uv run uvicorn app.main:app --reload
```

Useful local URLs:

-   API health check: http://127.0.0.1:8000/health
-   Interactive Swagger UI: http://127.0.0.1:8000/docs
-   ReDoc documentation: http://127.0.0.1:8000/redoc

Stop the development server with `Ctrl+C`.

### Run tests

From the project root:

``` powershell
uv run pytest -v
```

The current tests cover:

-   Health endpoint response
-   Successful product creation
-   Rejection of a negative product price
-   Rejection of a product request missing the required name

## Project Structure

``` text
Samaan/
├── app/
│   ├── main.py
│   ├── products_data.py
│   ├── routers/
│   │   └── products.py
│   └── schemas/
│       ├── ProductCreate.py
│       ├── ProductResponse.py
│       └── ProductUpdate.py
├── tests/
│   └── test_products.py
├── .gitignore
├── PROGRESS.md
├── pyproject.toml
└── uv.lock
```

## Current Limitations

-   Product data is stored in a Python list, so it is lost when the
    application restarts.
-   The in-memory store and product ID counter are not designed for
    concurrent or multi-process production use.
-   Test fixtures reset the shared product list, but do not reset the
    global product ID counter.
-   Authentication, authorization, database persistence, and production
    deployment are not implemented yet.

## Planned Roadmap

1.  Expand API tests for product listing, filtering, pagination, and
    CRUD edge cases.
2.  Introduce PostgreSQL, SQLAlchemy, and Alembic migrations.
3.  Add service-layer business logic and reliable transaction
    boundaries.
4.  Model warehouses, suppliers, purchase orders, inventory balances,
    and stock movements.
5.  Add automated tests for inventory invariants, partial receiving, and
    invalid stock transitions.
6.  Address concurrent stock updates and database locking.
7.  Add authentication, role-based access control, Docker, and
    deployment configuration.

## Development Workflow

Run the test suite before committing changes:

``` powershell
uv run pytest -v
```

Check the working tree and review changes before committing:

``` powershell
git status
git diff
```

This project is being developed incrementally as a hands-on learning
project. Documentation and roadmap items should be updated as features
are actually implemented.
