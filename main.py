from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from models import Produto

from database import listar_produtos
from database import inserir_produto
from database import buscar_produto_por_id
from database import sql_to_json
from database import deletar_produto
from database import atualizar_produto
from database import busca_filtro_nome
from database import sql_list_to_json
from database import buscar_produto_por_nome

app = FastAPI()


@app.get("/produtos")
async def get_produtos():
    resultados = listar_produtos()

    return sql_list_to_json(resultados)

@app.get("/produtos/{produto_id}")
async def get_produto(produto_id : int):
    produto = buscar_produto_por_id(produto_id)

    if produto is not None:
        produto = sql_to_json(produto)
        return produto
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado.')

@app.post("/produtos")
async def post_produto(produto : Produto):
    produto_por_id = buscar_produto_por_id(produto.id)
    produto_por_nome = buscar_produto_por_nome(produto.nome)
    
    if produto_por_id is not None or produto_por_nome is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID ou NOME do produto já existente.")
    
    inserir_produto(
        produto.id,
        produto.nome,
        produto.preco
        )
    
    return {
    "mensagem": "Produto criado com sucesso",
    "produto": produto
    }

@app.delete("/produtos/{produto_id}")
async def del_produto(produto_id : int):
    produto = buscar_produto_por_id(produto_id)
    produto_json = sql_to_json(produto)

    if produto is not None:
        deletar_produto(produto_id)
        return {
        "mensagem": "Produto removido com sucesso.",
        "produto": produto_json
        }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@app.put("/produtos/{produto_id}")
async def put_produto(produto_id : int, produto : Produto):
    produto_found = buscar_produto_por_id(produto_id)

    if produto_found is not None:
        produto.id = produto_id
        atualizar_produto(produto)

        produto_json = sql_to_json(buscar_produto_por_id(produto.id))

        return {
            "mensagem": "Produto alterado",
            "produto": produto_json
        }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto nao encontrado.')

@app.get("/busca")
async def get_teste(nome : str):
    resultados = busca_filtro_nome(nome)

    return sql_list_to_json(resultados)