from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session

# Importamos os arquivos voltando uma pasta (..) para achar a raiz
from database import get_db
from models import Produto_orm
from schemas import Produto

# Criamos o gerenciador de rotas com um prefixo e uma tag para organizar o Swagger
router = APIRouter(prefix="/produtos", tags=["Produtos"])

dbSession = Annotated[Session, Depends(get_db)]

@router.get("")
async def get_produtos(db: dbSession):
    resultados = db.query(Produto_orm).all()
    return resultados

@router.get("/{produto_id}")
async def get_produto(produto_id: int, db: dbSession):
    produto = db.query(Produto_orm).filter(Produto_orm.id == produto_id).first()
    if produto is not None:
        return produto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def post_produto(produto: Produto, db: dbSession):
    produto_por_id = db.query(Produto_orm).filter(Produto_orm.id == produto.id).first()
    produto_por_nome = db.query(Produto_orm).filter(Produto_orm.nome == produto.nome).first()
    
    if produto_por_id is not None or produto_por_nome is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID ou NOME do produto já existente.")
    
    novo_produto = Produto_orm(id=produto.id, nome=produto.nome, preco=produto.preco)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    return {
        "mensagem": "Produto criado com sucesso",
        "produto": novo_produto,
    }

@router.delete("/{produto_id}")
async def del_produto(produto_id: int, db: dbSession):
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
async def put_produto(produto_id: int, produto: Produto, db: dbSession):
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

@router.get("/busca/nome")
async def get_teste(nome: str, db: dbSession):
    termo_busca = f"%{nome}%"
    resultados = db.query(Produto_orm).filter(Produto_orm.nome.ilike(termo_busca)).all()
    return resultados