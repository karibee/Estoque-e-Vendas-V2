from sqlalchemy.orm import Session
from modules.products import repository
from models import Product_orm
from collections.abc import Sequence

class ProductNotFoundError(ValueError):
    """Raised when the requested product does not exist."""

def get_by_id(db: Session, product_id: int) -> Product_orm:
    product = repository.get_by_id(db, product_id)

    if product is None:
        raise ProductNotFoundError

    return product

def list_products(db: Session) -> Sequence[Product_orm]:
    return repository.list_all(db)