from sqlalchemy.orm import Session
from models import Produto_orm, Usuario_orm
from typing import Annotated, Optional
from fastapi import Depends
from database import get_db

dbSessionCrud = Annotated[Session, Depends(get_db)]

def get_produto_by_id(db: dbSessionCrud, produto_id : int):
    return db.query(Produto_orm).filter(Produto_orm.id == produto_id).first()

def get_produto_by_name(db: dbSessionCrud, produto_name : str):
    return db.query(Produto_orm).filter(Produto_orm.nome == produto_name).first()

def get_produto_by_donoID(db: dbSessionCrud, dono_id : int):
    return db.query(Usuario_orm).filter(Usuario_orm.id == dono_id).first()