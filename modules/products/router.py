from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from modules.users import repository as user_repository
from modules.products import repository as product_repository
from database import get_db
from models import Product_orm
from modules.products.schemas import Product
from modules.products import service

router = APIRouter(prefix="/products", tags=["Products"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("")
async def list_products(db: dbSession):
    return service.list_products(db)

@router.get("/{product_id}")
async def get_product(product_id: int, db: dbSession):
    try:
        return service.get_by_id(db, product_id)

    except service.ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.') from exc

@router.post("", status_code=status.HTTP_201_CREATED)
async def insert_product(product: Product, db: dbSession):
    try:
        new_product = service.create(db, product)
        return {
            "message": "Product created successfully",
            "product": new_product
        }

    except service.ProductConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Product ID or name already exists.') from exc

@router.post("/batch", status_code=status.HTTP_201_CREATED)
async def insert_products(products: List[Product], db: dbSession):
    results = []
    had_errors = False

    for product in products:
        product_by_id = product_repository.get_by_id(db, product.id)
        product_by_name = product_repository.get_by_name(db, product.name)
        
        if product_by_id is not None or product_by_name is not None:
            product_error = {
                 "name": f"{product.name}",
                 "error": "Product was not created: HTTP_409_CONFLICT"
                }

            results.append(product_error)
            had_errors = True
            continue
        
        new_product = Product_orm(id=product.id, owner_id=product.owner_id, name=product.name, price=product.price)
        db.add(new_product)
        
        results.append(new_product)

    db.commit()
    
    for item in results:
        if isinstance(item, Product_orm):
            db.refresh(item)

    if had_errors:
        return {
            "message": "Products processed with exceptions",
            "products": results,
        }
    
    return {
        "message": "Products created successfully",
        "products": results,
    }

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: dbSession):
    product = product_repository.get_by_id(db, product_id)
    if product is not None:
        db.delete(product)
        db.commit()
        return {
            "message": "Product removed successfully.",
            "product": product
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

@router.put("/{product_id}")
async def update_product(product_id: int, product: Product, db: dbSession):
    product_found = product_repository.get_by_id(db, product_id)
    if product_found is not None:
        product_found.name = product.name
        product_found.price = product.price
        db.commit()
        db.refresh(product_found)
        return {
            "message": "Product changed",
            "product": product_found
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

@router.put("/{product_id}")
async def update_product_owner(product_id: int, put_owner_id: int | None, db: dbSession):
    product_found = product_repository.get_by_id(db, product_id)
    if product_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    
    if put_owner_id is not None:
        check_owner_id = user_repository.get_by_id(db, put_owner_id)

        if check_owner_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User who will own the product not found.')

    product_found.owner_id = put_owner_id
    db.commit()
    db.refresh(product_found)
    return {
        "message": "Product changed",
        "product": product_found
    }

@router.get("/search/name")
async def get_test(name: str, db: dbSession):
    search_term = f"%{name}%"
    results = db.query(Product_orm).filter(Product_orm.name.ilike(search_term)).all()
    return results
