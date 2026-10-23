from pydantic import BaseModel,ConfigDict,Field

class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float=Field(ge=0)
    space_required: float=Field(gt=0)