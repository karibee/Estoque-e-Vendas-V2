from sqlalchemy.orm import Session
from models import Product_orm

def get_by_id(db: Session, product_id : int) -> Product_orm | None:
    return db.query(Product_orm).filter(Product_orm.id == product_id).first()

def get_by_name(db: Session, product_name : str) -> Product_orm | None:
    return db.query(Product_orm).filter(Product_orm.name == product_name).first()