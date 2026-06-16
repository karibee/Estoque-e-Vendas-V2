from models import Produto

produtos = [
    {
        "id": 1,
        "nome": "Mouse",
        "preco": 100
    },
    {
        "id": 2,
        "nome": "Teclado",
        "preco": 200
    }
]

def check_id(produto: Produto):
    for p in produtos:
        if produto.id == p['id'] or produto.nome == p['nome']:
            print('produto ja existe.')
            return

    produtos.append(
        {
        "id": produto.id,
        "nome": produto.nome
        }
    )

check_id()