from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models import User_orm
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[UserResponse])
async def list_users(db : dbSession):
    results = db.query(User_orm).all()
    return results

@router.post("", response_model=list[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(user : UserCreate, db : dbSession):
    user_by_id = db.query(User_orm).filter(User_orm.id == user.id).first()
    user_by_login = db.query(User_orm).filter(User_orm.login == user.login).first()
    
    if user_by_id is not None or user_by_login is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User ID or NAME already exists.")
    
    new_user = User_orm(id=user.id, login=user.login, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
