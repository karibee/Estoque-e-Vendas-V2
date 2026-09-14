from sqlalchemy.orm import Session
from modules.products import repository
from models import Product_orm
from modules.products.schemas import Product
from collections.abc import Sequence

class ProductConflictError(ValueError):
    """Raised when the product ID or name already exists"""

class ProductNotFoundError(ValueError):
    """Raised when the requested product does not exist."""

def get_by_id(db: Session, product_id: int) -> Product_orm:
    product = repository.get_by_id(db, product_id)

    if product is None:
        raise ProductNotFoundError

    return product

def list_products(db: Session) -> Sequence[Product_orm]:
    return repository.list_all(db)

def create(db: Session, product: Product) -> Product_orm:
    product_by_id = repository.get_by_id(db, product.id)
    product_by_name = repository.get_by_name(db, product.name)

    if product_by_id is not None or product_by_name is not None:
        raise ProductConflictError

    return repository.create(db, Product_orm(
        id=product.id, owner_id=product.owner_id, name=product.name, price=product.price
        ))