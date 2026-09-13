from sqlalchemy.orm import Session
from models import User_orm
from typing import Annotated
from fastapi import Depends
from database import get_db

dbSessionCrud = Annotated[Session, Depends(get_db)]

def get_product_by_ownerID(db: dbSessionCrud, owner_id : int):
    return db.query(User_orm).filter(User_orm.id == owner_id).first()
