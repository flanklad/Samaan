from pydantic import BaseModel

class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float| None = None
    space_required: float| None = None