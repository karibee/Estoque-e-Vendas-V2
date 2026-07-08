from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
import crud
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
    produto = crud.get_produto_by_id(db, produto_id)
    if produto is not None:
        return produto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def inserir_produto(produto: Produto, db: dbSession):
    produto_por_id = crud.get_produto_by_id(db, produto.id)
    produto_por_nome = crud.get_produto_by_name(db, produto.nome)
    
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

@router.post("/batch", status_code=status.HTTP_201_CREATED)
async def inserir_produtos(produtos: List[Produto], db: dbSession):
    resultados = []
    teve_erros = False

    for produto in produtos:
        produto_por_id = crud.get_produto_by_id(db, produto.id)
        produto_por_nome = crud.get_produto_by_name(db, produto.nome)
        
        if produto_por_id is not None or produto_por_nome is not None:
            produto_erro = {
                 "nome": f"{produto.nome}",
                 "erro": "Produto não foi criado : HTTP_409_CONFLICT"
                }

            resultados.append(produto_erro)
            teve_erros = True
            continue
        
        novo_produto = Produto_orm(id=produto.id, dono_id=produto.dono_id, nome=produto.nome, preco=produto.preco)
        db.add(novo_produto)
        
        resultados.append(novo_produto)

    db.commit()
    
    for item in resultados:
        if isinstance(item, Produto_orm):
            db.refresh(item)

    if teve_erros:
        return {
            "mensagem": "Produtos processados com exceções",
            "produtos": resultados,
        }
    
    return {
        "mensagem": "Produtos criados com sucesso",
        "produtos": resultados,
    }

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: int, db: dbSession):
    produto = crud.get_produto_by_id(db, produto_id)
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
    produto_found = crud.get_produto_by_id(db, produto_id) 
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
    produto_found = crud.get_produto_by_id(db, produto_id)
    if produto_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')
    
    if put_dono_id is not None:
        checar_dono_id = crud.get_produto_by_donoID(db, put_dono_id)

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

