from pydantic import BaseModel

class UserCreate(BaseModel):
    id : int
    login : str
    password : str

class UserResponse(BaseModel):
    id : int
    login : str

    model_config = {"from_attributes": True}
