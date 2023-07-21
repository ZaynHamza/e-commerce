from pydantic import BaseModel
from typing import Optional, List


class PostCategory(BaseModel):
    name: str


class PostProduct(BaseModel):
    name: str
    description: Optional[str]
    price: int
    category_id: int

