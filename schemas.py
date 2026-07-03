from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    id: int
    dono_id: Optional[int] = None
    nome: str
    preco : float

class UserCreate(BaseModel):
    id : int
    login : str
    senha : str

class UserResponse(BaseModel):
    id : int
    login : str

    model_config = {"from_attributes": True}