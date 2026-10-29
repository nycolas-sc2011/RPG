"""
jogadores.py - Funções da tabela JOGADORES (as pessoas que jogam).

Colunas: id, nome, apelido

TAREFA: complete as 4 funções. Use o arquivo classes.py como modelo.
Apague a linha "raise NotImplementedError" quando escrever o código.
"""


def incluir(conn, nome, apelido):
    """Insere um jogador e devolve o id gerado."""
    cursor = conn.execute(
        "INSERT INTO jogadores (nome, apelido) VALUES (?, ?)",
        (nome, apelido))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha (id, nome, apelido), ou None."""
    cursor = conn.execute("SELECT id, nome, apelido FROM jogadores WHERE id = ?",
                          (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com os jogadores cujo nome contém o texto."""
    cursor = conn.execute(
        "SELECT id, nome, apelido FROM jogadores WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todos os jogadores (id, nome, apelido)."""
    cursor = conn.execute("SELECT id, nome, apelido FROM jogadores ORDER BY id")
    return cursor.fetchall()
