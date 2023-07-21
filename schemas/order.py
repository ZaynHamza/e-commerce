from pydantic import BaseModel
from typing import Optional, List


class PostOrderItem(BaseModel):
    product_id: int
    quantity: int = 1


class PostOrder(BaseModel):
    client_name: str
    client_phone: str
    client_address: str
    items: List[PostOrderItem]
