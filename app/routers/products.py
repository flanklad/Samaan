from fastapi import APIRouter,Query,HTTPException
from app.schemas.ProductResponse import ProductResponse
from app.schemas.ProductCreate import ProductCreate
from app.schemas.ProductUpdate import ProductUpdate
from app.products_data import products
from app.services.products import list_products as list_products_service, create_product as create_product_service,find_product_by_id as find_product_service,update_product as update_product_service, delete_product as delete_product_service
router=APIRouter()



@router.get("/products", response_model=list[ProductResponse])
def get_products(category: str | None=None, skip: int =Query(default=0,ge=0),limit: int = Query(default=10,ge=1, le=100)):
    return list_products_service(
        category=category,
        skip=skip,
        limit=limit,
    )

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int):
    product = find_product_service(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found",
        )
    return product

@router.post("/products",status_code=201)
def add_product(product:ProductCreate):
    return create_product_service(product)


@router.patch("/products/{product_id}",response_model= ProductResponse)
def update_product(product_id: int ,update_data:ProductUpdate):
    updates=update_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code=400,
            detail="Fields cannot be null",
        )

    updated_product= update_product_service(product_id,updates)

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return updated_product

@router.delete("/products/{product_id}",status_code=204)
def delete_product(product_id:int):
    product_deleted=delete_product_service(product_id)

    if not product_deleted:
        raise HTTPException(status_code=404,detail="Product Not Found")

    return None

