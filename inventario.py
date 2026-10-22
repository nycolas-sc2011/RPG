"""
inventario.py - Funções da tabela INVENTARIO.   (DESAFIO)

Colunas: id, personagem_id, item_id, quantidade

Cada linha do inventário diz que um PERSONAGEM carrega um ITEM, em uma
certa quantidade. A busca "por nome" deve procurar pelo nome do PERSONAGEM.

As consultas devem devolver as colunas nesta ordem:
    (id, nome do personagem, nome do item, tipo do item, quantidade)

TAREFA: escreva a CONSULTA (com dois JOINs) e complete as 4 funções.
Dica: o arquivo personagens.py faz algo muito parecido.
"""

CONSULTA = """
    -- TODO: SELECT ... FROM inventario JOIN personagens ... JOIN itens ...
"""


def incluir(conn, personagem_id, item_id, quantidade):
    """Coloca um item no inventário de um personagem e devolve o id gerado."""
    # TODO
    raise NotImplementedError


def buscar_por_id(conn, id):
    """Devolve UMA linha, ou None."""
    # TODO
    raise NotImplementedError


def buscar_por_nome(conn, nome_personagem):
    """Devolve uma LISTA com os itens dos personagens cujo nome contém o texto."""
    # TODO
    raise NotImplementedError


def listar(conn):
    """Devolve uma LISTA com todo o inventário."""
    # TODO
    raise NotImplementedError
