import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.products_data import products
from app.schemas.ProductResponse import ProductResponse

client = TestClient(app)# will send request to app

@pytest.fixture
def reset_product_data():
 products.clear()

 yield

 products.clear()



def test_health():
 response= client.get("/health")
 assert response.status_code== 200
 assert response.json()== { "status" : "healthy"}


product_data = {
    "name": "Keyboard",
    "category": "Electronics",
    "price": 50.0,
    "space_required": 2.0
}
product_data_negative_price = {
    "name": "Keyboard",
    "category": "Electronics",
    "price": -50.0,
    "space_required": 2.0
}
invalid_product = {
    "category": "Electronics",
    "price": 50.0,
    "space_required": 2.0
}

def test_add_product(reset_product_data):
 response=client.post("/products",json=product_data)
 assert "id" in response.json()
 assert response.status_code==201
 assert response.json()["name"] == "Keyboard"
 assert response.json()["category"] =="Electronics"
 assert response.json()["price"] == 50.0
 assert response.json()["space_required"]==2.0


def test_add_products_rejects_negative_price(reset_product_data):
 response= client.post("/products",json=product_data_negative_price)
 assert response.status_code == 422


def test_add_product_rejects_missing_name(reset_product_data):
 response=client.post("/products",json=invalid_product)
 assert response.status_code==422

def test_list_products(reset_product_data):
    product_get = ProductResponse(
        id=1,
        name="Keyboard",
        category="Electronics",
        price=50.0,
        space_required=2.0
    )

    products.append(product_get)
    response =client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"]=="Keyboard"

def test_list_products_filters_by_category(reset_product_data):
    keyboard = ProductResponse(
        id=1,
        name="Keyboard",
        category="Electronics",
        price=50.0,
        space_required=2.0
    )

    mouse = ProductResponse(
        id=2,
        name="Mouse",
        category="Electronics",
        price=20.0,
        space_required=1.0
    )

    chair = ProductResponse(
        id=3,
        name="Chair",
        category="Furniture",
        price=120.0,
        space_required=8.0
    )
    products.extend([keyboard,mouse,chair])
    response = client.get("/products",params={"category":"Electronics"})

    assert response.status_code==200
    data= response.json()
    assert len(data)==2

    assert all(
        product["category"]=="Electronics"
        for product in data
    )

def test_list_products_pagination(reset_product_data):
        # Arrange: create five products in a known order.
        keyboard = ProductResponse(
            id=1, name="Keyboard", category="Electronics",
            price=50.0, space_required=2.0
        )
        mouse = ProductResponse(
            id=2, name="Mouse", category="Electronics",
            price=20.0, space_required=1.0
        )
        monitor = ProductResponse(
            id=3, name="Monitor", category="Electronics",
            price=200.0, space_required=4.0
        )
        chair = ProductResponse(
            id=4, name="Chair", category="Furniture",
            price=120.0, space_required=8.0
        )
        desk = ProductResponse(
            id=5, name="Desk", category="Furniture",
            price=150.0, space_required=10.0
        )

        # Add the products in the order the test expects.
        products.extend([keyboard, mouse, monitor, chair, desk])

        # Act: skip two products and request the next two.
        response = client.get(
            "/products",
            params={"skip": 2, "limit": 2}
        )
        # Assert: verify the request succeeded.
        assert response.status_code == 200
        # Decode the response JSON into a Python list.
        data = response.json()
        # Verify that pagination returned exactly two products.
        assert len(data) == 2
        # Verify the correct products were returned, in order.
        assert data[0]["name"] == "Monitor"
        assert data[1]["name"] == "Chair"


def test_list_products_returns_empty_list_when_no_match(reset_product_data):

    keyboard = ProductResponse(
        id=1,
        name="Keyboard",
        category="Electronics",
        price=50.0,
        space_required=2.0
    )
    products.append(keyboard)
    response = client.get(
        "/products",
        params={"category": "Furniture"}
    )
    assert response.status_code == 200
    assert response.json() == []

def test_list_products_rejects_negative_skip(reset_product_data):
    response = client.get(
        "/products",
        params={"skip": -1}
    )

    assert response.status_code == 422

def test_list_products_rejects_limit_above_maximum(reset_product_data):
    # Act: request more products than the allowed maximum.
    response = client.get(
        "/products",
        params={"limit": 101}
    )
    assert response.status_code == 422

def test_get_product_by_id(reset_product_data):
    # Arrange: create a product through the POST endpoint.
    product_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "space_required": 2.5,
    }
    create_response=client.post("/products",json=product_data)

    product_id=create_response.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    returned_product = response.json()

    assert returned_product["id"] == product_id
    assert returned_product["name"] == "Laptop"
    assert returned_product["category"] == "Electronics"
    assert returned_product["price"] == 75000
    assert returned_product["space_required"] == 2.5

def test_get_product_by_id_returns_404_when_not_found(reset_product_data):
    response=client.get("/products/999")
    assert response.status_code==404
    assert response.json() == {"detail": "Product Not Found"}

def test_patch_product_updates_only_supplied_fields(reset_product_data):
    product_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "space_required": 2.5,
    }
    create_response=client.post("/products",json=product_data)
    product_id=create_response.json()["id"]

    response =client.patch(
        f"/products/{product_id}",
        json={"price":70000}
    )

    assert response.status_code==200

    updated_product=response.json()
    # Verify that the supplied field changed.
    assert updated_product["price"] == 70000

    # Verify that fields not supplied remain unchanged.
    assert updated_product["id"] == product_id
    assert updated_product["name"] == "Laptop"
    assert updated_product["category"] == "Electronics"
    assert updated_product["space_required"] == 2.5


def test_patch_product_rejects_empty_update(reset_product_data):
    product_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "space_required": 2.5,
    }
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No fields provided for update"
    }

def test_patch_product_rejects_null_values(reset_product_data):
    product_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "space_required": 2.5,
    }
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    response=client.patch(f"/products/{product_id}",json={"name":None})

    assert response.status_code==400
    assert response.json()=={"detail":"Fields cannot be null"}

def test_patch_product_returns_404_when_not_found(reset_product_data):
    # Act: attempt to update a product that does not exist.
    response = client.patch(
        "/products/999",
        json={"price": 70000},
    )

    # Assert: the API returns HTTP 404 Not Found.
    assert response.status_code == 404

    # Assert: the response contains the expected error detail.
    assert response.json() == {
        "detail": "Product Not Found"
    }

def test_delete_product_successfully(reset_product_data):
    product_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "space_required": 2.5,
    }
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    response=client.delete(f"/products{product_id}")
    # Assert: deletion was successful.
    assert response.status_code == 204

    # Verify that the product no longer exists.
    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Product Not Found"
    }
def test_delete_product_returns_404_when_not_found(reset_product_data):
    # Act: attempt to delete a product that doesn't exist.
    response = client.delete("/products/999")

    # Assert: the API returns HTTP 404.
    assert response.status_code == 404

    # Verify the error response.
    assert response.json() == {
        "detail": "Product Not Found"
    }







