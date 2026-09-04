from sqlalchemy.orm import Session
from models import Product_orm, User_orm
from typing import Annotated, Optional
from fastapi import Depends
from database import get_db

dbSessionCrud = Annotated[Session, Depends(get_db)]

def get_product_by_id(db: dbSessionCrud, product_id : int):
    return db.query(Product_orm).filter(Product_orm.id == product_id).first()

def get_product_by_name(db: dbSessionCrud, product_name : str):
    return db.query(Product_orm).filter(Product_orm.name == product_name).first()

def get_product_by_ownerID(db: dbSessionCrud, owner_id : int):
    return db.query(User_orm).filter(User_orm.id == owner_id).first()

def user_by_id(db: dbSessionCrud, user_id: int) -> User_orm | None:
    return db.query(User_orm).filter(User_orm.id == user_id).first()