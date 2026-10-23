from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    space_required: float