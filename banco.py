"""
banco.py - Conexão com o banco de dados e criação das tabelas.

Usamos o SQLite, que já vem junto com o Python: o banco inteiro fica
guardado em um único arquivo (rpg.db), criado na primeira vez que o
programa roda. Não é preciso instalar nada.
"""

import sqlite3

NOME_ARQUIVO = "rpg.db"


def conectar(nome_arquivo=NOME_ARQUIVO):
    """Abre (ou cria) o arquivo do banco e devolve a conexão."""
    conn = sqlite3.connect(nome_arquivo)
    # Liga a verificação de chaves estrangeiras (no SQLite ela vem desligada)
    conn.execute("PRAGMA foreign_keys = ON")
    criar_tabelas(conn)
    return conn


def criar_tabelas(conn):
    """Cria as 5 tabelas, se ainda não existirem."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS classes (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nome  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jogadores (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            apelido  TEXT
        );

        CREATE TABLE IF NOT EXISTS itens (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nome   TEXT NOT NULL,
            tipo   TEXT,
            poder  INTEGER
        );

        CREATE TABLE IF NOT EXISTS personagens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT NOT NULL,
            nivel       INTEGER,
            jogador_id  INTEGER NOT NULL REFERENCES jogadores(id),
            classe_id   INTEGER NOT NULL REFERENCES classes(id)
        );

        CREATE TABLE IF NOT EXISTS inventario (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            personagem_id  INTEGER NOT NULL REFERENCES personagens(id),
            item_id        INTEGER NOT NULL REFERENCES itens(id),
            quantidade     INTEGER NOT NULL
        );
    """)
    conn.commit()


def carregar_exemplos(conn):
    """Coloca alguns registros de exemplo no banco (só se ele estiver vazio)."""
    total = conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
    if total > 0:
        return False

    conn.executemany("INSERT INTO classes (nome) VALUES (?)",
                     [("Guerreiro",), ("Mago",), ("Arqueiro",), ("Curandeiro",)])
    conn.executemany("INSERT INTO jogadores (nome, apelido) VALUES (?, ?)",
                     [("Ana Souza", "DragaoAzul"), ("Bruno Lima", "Bru"),
                      ("Carla Mendes", "CarlaGamer"), ("Diego Rocha", "Rochedo")])
    conn.executemany("INSERT INTO itens (nome, tipo, poder) VALUES (?, ?, ?)",
                     [("Espada Longa", "Arma", 30),
                      ("Cajado de Fogo", "Arma", 35),
                      ("Arco Élfico", "Arma", 28),
                      ("Poção de Vida", "Poção", 50),
                      ("Escudo de Ferro", "Armadura", 20)])
    conn.executemany(
        "INSERT INTO personagens (nome, nivel, jogador_id, classe_id) VALUES (?, ?, ?, ?)",
        [("Gork", 5, 1, 1),
         ("Zéfira", 7, 2, 2),
         ("Flecha Veloz", 3, 3, 3),
         ("Luna", 4, 1, 4),
         ("Brasa", 2, 4, 2)])
    conn.executemany(
        "INSERT INTO inventario (personagem_id, item_id, quantidade) VALUES (?, ?, ?)",
        [(1, 1, 1), (1, 4, 3), (2, 2, 1), (3, 3, 1), (4, 4, 5), (1, 5, 1)])
    conn.commit()
    return True
