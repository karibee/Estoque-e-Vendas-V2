from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from typing import Annotated

from sqlalchemy.orm import Session

from models import Produto

import database_orm
import models_orm

app = FastAPI()

DbSession = Annotated[Session, Depends(database_orm.get_db)]

@app.get("/produtos")
async def get_produtos(db: DbSession):
    resultados = db.query(models_orm.Produto_orm).all()

    return resultados

@app.get("/produtos/{produto_id}")
async def get_produto(produto_id : int, db: DbSession):
    produto = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.id == produto_id).first()

    if produto is not None:
        return produto
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@app.post("/produtos", status_code=status.HTTP_201_CREATED)
async def post_produto(produto : Produto, db: DbSession):
    produto_por_id = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.id == produto.id).first()
    produto_por_nome = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.nome == produto.nome).first()
    
    if produto_por_id is not None or produto_por_nome is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID ou NOME do produto já existente.")
    
    novo_produto = models_orm.Produto_orm(id=produto.id, nome=produto.nome, preco=produto.preco)

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    return {
    "mensagem": "Produto criado com sucesso",
    "produto": novo_produto,
    }

@app.delete("/produtos/{produto_id}")
async def del_produto(produto_id : int, db : DbSession):
    produto = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.id == produto_id).first()

    if produto is not None:
        db.delete(produto)
        db.commit()
        
        return {
        "mensagem": "Produto removido com sucesso.",
        "produto": produto
        }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@app.put("/produtos/{produto_id}")
async def put_produto(produto_id : int, produto : Produto, db : DbSession):
    produto_found = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.id == produto_id).first() 

    if produto_found is not None:
        produto_found.nome = produto.nome
        produto_found.preco = produto.preco
        
        db.commit()
        db.refresh(produto_found)

        return {
            "mensagem": "Produto alterado",
            "produto": produto_found
        }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@app.get("/busca")
async def get_teste(nome : str, db : DbSession):
    termo_busca = f"%{nome}%"

    resultados = db.query(models_orm.Produto_orm).filter(models_orm.Produto_orm.nome.ilike(termo_busca)).all()

    return resultados