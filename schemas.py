from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    owner_id: Optional[int] = None
    name: str
    price : float

class UserCreate(BaseModel):
    id : int
    login : str
    password : str

class UserResponse(BaseModel):
    id : int
    login : str

    model_config = {"from_attributes": True}
