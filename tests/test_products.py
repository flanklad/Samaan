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
