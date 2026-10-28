from app.products_data import products
from app.schemas.ProductResponse import ProductResponse

def get_all_products() -> list[ProductResponse]:
    return list(products)

