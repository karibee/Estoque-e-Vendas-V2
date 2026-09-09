from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models import User_orm
from modules.users.schemas import UserCreate, UserResponse
from modules.users import repository

router = APIRouter(prefix="/users", tags=["Users"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[UserResponse])
async def list_users(db : dbSession):
    return repository.list_all(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(db : dbSession, user_id : int):
    user = repository.get_by_id(db, user_id)

    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user : UserCreate, db : dbSession):
    user_from_id = repository.get_by_id(db, user.id)
    user_from_login = repository.get_by_login(db, user.login)
    
    if user_from_id is not None or user_from_login is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User ID or LOGIN already exists.")
    
    new_user = User_orm(id=user.id, login=user.login, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
