from fastapi import APIRouter,Query,HTTPException
from app.schemas.ProductResponse import ProductResponse
from app.schemas.ProductCreate import ProductCreate
from app.schemas.ProductUpdate import ProductUpdate
from app.products_data import products


router=APIRouter()

next_product_id =1

@router.get("/products", response_model=list[ProductResponse])
def get_products(category: str | None=None, skip: int =Query(default=0,ge=0),limit: int = Query(default=10,ge=1, le=100)):

    if category is not None:
        filtered_products=[product for product in products
                           if product.category==category
                           ]
    else:
        filtered_products=products

    return filtered_products[skip:skip+limit]

@router.get("/products/{product_id}",response_model=ProductResponse)
def get_product_by_id(product_id:int):
    for product in products:
        if product.id==product_id:
            return product

    raise HTTPException(status_code=404,detail="Product Not Found")

@router.post("/products",status_code=201)
def add_product(product:ProductCreate):
    new_id= len(products)+1

    newProduct=ProductResponse(
    id=new_id,
    name = product.name,
    category = product.category,
    price=product.price,
    space_required=product.space_required
    )
    products.append(newProduct)
    return newProduct

@router.post("/products",status_code=201)
def add_product(product:ProductCreate):
    new_id= len(products)+1

    newProduct=ProductResponse(
    id=new_id,
    name = product.name,
    category = product.category,
    price=product.price,
    space_required=product.space_required
    )
    products.append(newProduct)
    return newProduct


@router.patch("/products/{product_id}",response_model= ProductResponse)
def update_product(product_id: int ,update_data:ProductUpdate):
    product= None
    for item in products:
        if item.id==product_id:
            product= item
            break

    if product is None:
        raise HTTPException(
            status_code= 404,
            detail="Product Not Found"
        )

    changes = update_data.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code = 400,
            detail= "No fields provided for update"
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(status_code=422,
                            detail="Product fields cannot be null"
                         )

    for field,value in changes.items():
        setattr(product,field,value)

    return product

@router.delete("/products/{product_id}",status_code=204)
def delete_product(product_id:int):
    product=None
    for item in products:
        if item.id==product_id:
            product= item
            break

    if product is None:
        raise HTTPException(status_code=404,detail="Product Not Found")

    products.remove(product)
    return None