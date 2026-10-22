"""
classes.py - Funções da tabela CLASSES (Guerreiro, Mago, ...).

Colunas: id, nome

Este é o ARQUIVO-MODELO: use-o como exemplo para escrever os outros.
Toda função recebe a conexão (conn) como primeiro parâmetro.
"""


def incluir(conn, nome):
    """Insere uma classe e devolve o id que o banco gerou para ela."""
    cursor = conn.execute("INSERT INTO classes (nome) VALUES (?)", (nome,))
    conn.commit()                 # grava de verdade no arquivo
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha (id, nome), ou None se o id não existir."""
    cursor = conn.execute("SELECT id, nome FROM classes WHERE id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com as classes cujo nome contém o texto digitado."""
    cursor = conn.execute(
        "SELECT id, nome FROM classes WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todas as classes."""
    cursor = conn.execute("SELECT id, nome FROM classes ORDER BY id")
    return cursor.fetchall()