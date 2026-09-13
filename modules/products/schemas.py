from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    owner_id: Optional[int] = None
    name: str
    price : float
