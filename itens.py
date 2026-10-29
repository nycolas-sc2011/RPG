"""
itens.py - Funções da tabela ITENS (armas, poções, armaduras...).

Colunas: id, nome, tipo, poder, descricao

TAREFA: complete as 4 funções. Use o arquivo classes.py como modelo.
Apague a linha "raise NotImplementedError" quando escrever o código.
"""


def incluir(conn, nome, tipo, poder, descricao=""):
    """Insere um item e devolve o id gerado."""
    cursor = conn.execute(
        "INSERT INTO itens (nome, tipo, poder, descricao) VALUES (?, ?, ?, ?)",
        (nome, tipo, poder, descricao))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha com os dados do item, ou None."""
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder, descricao FROM itens WHERE id = ?",
        (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com os itens cujo nome contém o texto."""
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder, descricao FROM itens "
        "WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def buscar_por_tipo(conn, tipo):
    """Devolve uma LISTA com os itens cujo tipo contém o texto."""
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder, descricao FROM itens "
        "WHERE tipo LIKE ? ORDER BY nome",
        ("%" + tipo + "%",))
    return cursor.fetchall()


def definir_classe_do_tipo(conn, tipo, classe_id):
    """Define qual classe pode usar um tipo de item."""
    cursor = conn.execute(
        "SELECT tipo FROM restricoes_tipos WHERE tipo = ?", (tipo,))
    if cursor.fetchone():
        conn.execute(
            "UPDATE restricoes_tipos SET classe_id = ? WHERE tipo = ?",
            (classe_id, tipo))
    else:
        conn.execute(
            "INSERT INTO restricoes_tipos (tipo, classe_id) VALUES (?, ?)",
            (tipo, classe_id))
    conn.commit()


def remover_classe_do_tipo(conn, tipo):
    """Remove a restrição de classe de um tipo de item."""
    conn.execute("DELETE FROM restricoes_tipos WHERE tipo = ?", (tipo,))
    conn.commit()


def listar(conn):
    """Devolve uma LISTA com todos os itens."""
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder, descricao FROM itens ORDER BY id")
    return cursor.fetchall()
