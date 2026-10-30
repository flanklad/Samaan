from app.products_data import products
from app.schemas.ProductResponse import ProductResponse
from app.schemas.ProductCreate import ProductCreate

def get_all_products() -> list[ProductResponse]:
    return list(products)

def create_product(product_data: ProductCreate)-> ProductResponse:
    next_product_id= len(products)+1
    new_product=ProductResponse(
        id=next_product_id,
        **product_data.model_dump()
    )
    products.append(new_product)
    return new_product

def find_product(product_id:int)-> ProductResponse | None:
    for product in products:
        if product.id==product_id:
            return product
    return None

#provide a dictionary of updates to be done
def update_product(product_id:int,updates: dict[str,object],)-> ProductResponse | None:
    for product in products:
        if product.id==product_id:
             for field,value in updates.items():
                 setattr(product,field,value) #Product.field=value

             return product
    return None

def delete_product(product_id:int)-> bool:
    for product in products:
        if product.id==product_id:
            products.remove(product)
            return True
    return False


