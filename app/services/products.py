from _pytest.config import findpaths

from app.repositories.products import get_all_products as get_all_products_record
from app.schemas.ProductCreate import ProductCreate
from app.schemas.ProductResponse import ProductResponse
from app.repositories.products import create_product as create_product_record,find_product as find_product_record, update_product as update_product_record, delete_product as delete_product_record

def list_products(
    category: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[ProductResponse]:
    # Retrieve the products from the repository.
    all_products = get_all_products_record()

    # Apply the category filter only when the client supplied one.
    if category is not None:
        all_products = [
            product
            for product in all_products
            if product.category == category
        ]
    # Skip the requested number of matching products and return
    # at most 'limit' products.
    return all_products[skip : skip + limit]

def create_product(product_data:ProductCreate)-> ProductResponse:
    return create_product_record(product_data)

def find_product_by_id(product_id:int) -> ProductResponse | None:
    return find_product_record(product_id)

def update_product(product_id,updates:dict[str,object])-> ProductResponse | None:
    return update_product_record(product_id,updates)

def delete_product(product_id:int)-> bool:
    return delete_product_record(product_id)