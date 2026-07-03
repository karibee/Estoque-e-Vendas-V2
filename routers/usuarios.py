from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario_orm
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[UserResponse])
async def listar_usuarios(db : dbSession):
    resultados = db.query(Usuario_orm).all()
    return resultados

@router.post("", response_model=list[UserResponse], status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario : UserCreate, db : dbSession):
    usuario_por_id = db.query(Usuario_orm).filter(Usuario_orm.id == usuario.id).first()
    usuario_por_login = db.query(Usuario_orm).filter(Usuario_orm.nome == usuario.nome).first()
    
    if usuario_por_id is not None or usuario_por_login is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID ou NOME do usuario já existente.")
    
    novo_usuario = Usuario_orm(id=usuario.id, login=usuario.login, senha=usuario.senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)