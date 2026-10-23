import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.products_data import products

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