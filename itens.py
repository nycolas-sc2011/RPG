"""
itens.py - Funções da tabela ITENS (armas, poções, armaduras...).

Colunas: id, nome, tipo, poder

TAREFA: complete as 4 funções. Use o arquivo classes.py como modelo.
Apague a linha "raise NotImplementedError" quando escrever o código.
"""


def incluir(conn, nome, tipo, poder):
    """Insere um item e devolve o id gerado."""
    # TODO
    raise NotImplementedError


def buscar_por_id(conn, id):
    """Devolve UMA linha (id, nome, tipo, poder), ou None."""
    # TODO
    raise NotImplementedError


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com os itens cujo nome contém o texto."""
    # TODO
    raise NotImplementedError


def listar(conn):
    """Devolve uma LISTA com todos os itens (id, nome, tipo, poder)."""
    # TODO
    raise NotImplementedError
