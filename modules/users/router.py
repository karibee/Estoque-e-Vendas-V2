from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from modules.users.schemas import UserCreate, UserResponse
from modules.users import service
from modules.users import repository

router = APIRouter(prefix="/users", tags=["Users"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[UserResponse])
async def list_users(db : dbSession):
    return repository.list_all(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(db : dbSession, user_id : int):
    try:
        user = service.get_user(db, user_id)
        return user

    except service.UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found') from exc

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user : UserCreate, db : dbSession):
    try:
        created_user = service.create(db, user)
        return created_user
    
    except service.UserConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User login or ID already exists') from exc
