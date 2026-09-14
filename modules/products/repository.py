from sqlalchemy.orm import Session
from models import Product_orm
from collections.abc import Sequence

def get_by_id(db: Session, product_id : int) -> Product_orm | None:
    return db.query(Product_orm).filter(Product_orm.id == product_id).first()

def get_by_name(db: Session, product_name : str) -> Product_orm | None:
    return db.query(Product_orm).filter(Product_orm.name == product_name).first()

def list_all(db: Session) -> Sequence[Product_orm]:
    return db.query(Product_orm).all()

def create(db: Session, new_product: Product_orm) -> Product_orm:
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product