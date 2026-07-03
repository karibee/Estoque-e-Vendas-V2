from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
from models import Produto_orm, Usuario_orm
from schemas import Produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("")
async def listar_produtos(db: dbSession):
    resultados = db.query(Produto_orm).all()
    return resultados

@router.get("/{produto_id}")
async def get_produto(produto_id: int, db: dbSession):
    produto = db.query(Produto_orm).filter(Produto_orm.id == produto_id).first()
    if produto is not None:
        return produto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def inserir_produto(produto: Produto, db: dbSession):
    produto_por_id = db.query(Produto_orm).filter(Produto_orm.id == produto.id).first()
    produto_por_nome = db.query(Produto_orm).filter(Produto_orm.nome == produto.nome).first()
    
    if produto_por_id is not None or produto_por_nome is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID ou NOME do produto já existente.")
    
    novo_produto = Produto_orm(id=produto.id, dono_id=produto.dono_id, nome=produto.nome, preco=produto.preco)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    return {
        "mensagem": "Produto criado com sucesso",
        "produto": novo_produto,
    }

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: int, db: dbSession):
    produto = db.query(Produto_orm).filter(Produto_orm.id == produto_id).first()
    if produto is not None:
        db.delete(produto)
        db.commit()
        return {
            "mensagem": "Produto removido com sucesso.",
            "produto": produto
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@router.put("/{produto_id}")
async def atualizar_produto(produto_id: int, produto: Produto, db: dbSession):
    produto_found = db.query(Produto_orm).filter(Produto_orm.id == produto_id).first() 
    if produto_found is not None:
        produto_found.nome = produto.nome
        produto_found.preco = produto.preco
        db.commit()
        db.refresh(produto_found)
        return {
            "mensagem": "Produto alteredo",
            "produto": produto_found
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@router.put("/{produto_id}")
async def atualizar_dono_produto(produto_id: int, put_dono_id: int | None, db: dbSession):
    produto_found = db.query(Produto_orm).filter(Produto_orm.id == produto_id).first()

    if produto_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')
    
    if put_dono_id is not None:
        checar_dono_id = db.query(Usuario_orm).filter(Usuario_orm.id == put_dono_id).first()

        if checar_dono_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario a ser dono do produto não encontrado.')

    produto_found.dono_id = put_dono_id
    db.commit()
    db.refresh(produto_found)
    return {
        "mensagem": "Produto alteredo",
        "produto": produto_found
    }

@router.get("/busca/nome")
async def get_teste(nome: str, db: dbSession):
    termo_busca = f"%{nome}%"
    resultados = db.query(Produto_orm).filter(Produto_orm.nome.ilike(termo_busca)).all()
    return resultados

