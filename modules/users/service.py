from modules.users.schemas import UserCreate
from models import User_orm
from sqlalchemy.orm import Session
from modules.users import repository

class UserConflictError(ValueError):
    """Raised when a user login or ID already exists"""

def create(db: Session, user: UserCreate) -> User_orm:
    user_from_id = repository.get_by_id(db, user.id)
    user_from_login = repository.get_by_login(db, user.login)
    
    if user_from_id is not None or user_from_login is not None:
        raise UserConflictError
    
    return repository.create(db, User_orm(id=user.id, login=user.login, password=user.password))