from collections.abc import Sequence
from models import User_orm
from sqlalchemy.orm import Session

def get_by_id(db: Session, user_id: int) -> User_orm | None:
    return db.query(User_orm).filter(User_orm.id == user_id).first()

def get_by_login(db: Session, user_login: str) -> User_orm | None:
    return db.query(User_orm).filter(User_orm.login == user_login).first()

def list_all(db: Session) -> Sequence[User_orm]:
    return db.query(User_orm).all()