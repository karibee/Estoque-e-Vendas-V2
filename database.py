import sqlite3
from models import Produto

conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()

def criar_tabela():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            preco REAL NOT NULL       
            )
        """
    )
    
def listar_produtos():
    cursor.execute(
        """
        SELECT * FROM produtos
        """
    )

    return cursor.fetchall()

def inserir_produto(id, nome, preco):
    cursor.execute(
        """
        INSERT INTO produtos
        (id, nome, preco)
        VALUES (?, ?, ?)
        """,
        (id, nome, preco)
    )

    conexao.commit()

def buscar_produto_por_id(produto_id):
    cursor.execute(
        """
        SELECT * FROM produtos
        WHERE id = ?
        """,
        (produto_id,)
    )
    return cursor.fetchone()

def buscar_produto_por_nome(produto_nome):
    cursor.execute(
        """
        SELECT * FROM produtos
        WHERE nome = ?
        """,
        (produto_nome,)
    )
    return cursor.fetchone()

def busca_filtro_nome(produto_nome : str):
    cursor.execute(
        """
        SELECT * FROM produtos
        WHERE nome LIKE ?
        """,
        (f"%{produto_nome}%",)
    )
    return cursor.fetchall()

def deletar_produto(produto_id):
    cursor.execute(
        """
        DELETE FROM produtos
        WHERE id = ?
        """,
        (produto_id,)
    )
    conexao.commit()

def atualizar_produto(produto : Produto):
    cursor.execute(
        """
        UPDATE produtos
        SET nome = ?, preco = ?
        WHERE id = ?
        """,
        (produto.nome, produto.preco, produto.id)
    )
    conexao.commit()

def sql_to_json(sql_produto : tuple):
    if sql_produto is None:
        return None
    
    produto_json = {
        "id" : sql_produto[0],
        "nome" : sql_produto[1],
        "preco" : sql_produto [2]
    }
    return produto_json

def sql_list_to_json(lista_produtos : list):
    resultados_json = []

    for produto in lista_produtos:
        produto = sql_to_json(produto)
        resultados_json.append(produto)

    return resultados_json

criar_tabela()