from app.repositories.products import get_all_products
from app.schemas.ProductResponse import ProductResponse

def list_products(
    category: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[ProductResponse]:
    # Retrieve the products from the repository.
    all_products = get_all_products()

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
