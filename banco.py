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
    """Cria as tabelas e atualiza itens antigos, se necessário."""
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
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            tipo      TEXT,
            poder     INTEGER,
            descricao TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS restricoes_tipos (
            tipo      TEXT PRIMARY KEY COLLATE NOCASE,
            classe_id INTEGER NOT NULL REFERENCES classes(id)
        );

        CREATE TABLE IF NOT EXISTS personagens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT NOT NULL,
            nivel       INTEGER,
            energia     INTEGER NOT NULL DEFAULT 0,
            jogador_id  INTEGER NOT NULL REFERENCES jogadores(id),
            classe_id   INTEGER NOT NULL REFERENCES classes(id)
        );

        CREATE TABLE IF NOT EXISTS magias (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            nivel     INTEGER NOT NULL,
            poder     INTEGER NOT NULL,
            descricao TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS personagem_magias (
            personagem_id INTEGER NOT NULL REFERENCES personagens(id),
            magia_id      INTEGER NOT NULL REFERENCES magias(id),
            nivel_personagem INTEGER NOT NULL,
            PRIMARY KEY (personagem_id, nivel_personagem)
        );

        CREATE TABLE IF NOT EXISTS inventario (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            personagem_id  INTEGER NOT NULL REFERENCES personagens(id),
            item_id        INTEGER NOT NULL REFERENCES itens(id),
            quantidade     INTEGER NOT NULL
        );
    """)

    colunas = conn.execute("PRAGMA table_info(itens)").fetchall()
    if "descricao" not in [coluna[1] for coluna in colunas]:
        conn.execute(
            "ALTER TABLE itens ADD COLUMN descricao TEXT NOT NULL DEFAULT ''")

    colunas = conn.execute("PRAGMA table_info(personagens)").fetchall()
    if "energia" not in [coluna[1] for coluna in colunas]:
        conn.execute(
            "ALTER TABLE personagens ADD COLUMN energia INTEGER NOT NULL DEFAULT 0")

    classes = conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
    if classes > 0:
        feiticeiro = conn.execute(
            "SELECT id FROM classes WHERE nome = ? COLLATE NOCASE",
            ("Feiticeiro",)).fetchone()
        if feiticeiro is None:
            conn.execute("INSERT INTO classes (nome) VALUES (?)", ("Feiticeiro",))

    conn.commit()


def carregar_exemplos(conn):
    """Coloca alguns registros de exemplo no banco (só se ele estiver vazio)."""
    total = conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
    if total > 0:
        return False

    conn.executemany("INSERT INTO classes (nome) VALUES (?)",
                     [("Guerreiro",), ("Mago",), ("Arqueiro",),
                      ("Curandeiro",), ("Feiticeiro",)])
    conn.executemany("INSERT INTO jogadores (nome, apelido) VALUES (?, ?)",
                     [("Ana Souza", "DragaoAzul"), ("Bruno Lima", "Bru"),
                      ("Carla Mendes", "CarlaGamer"), ("Diego Rocha", "Rochedo")])
    conn.executemany(
        "INSERT INTO itens (nome, tipo, poder, descricao) VALUES (?, ?, ?, ?)",
        [("Espada Longa", "Arma", 30, "Uma espada de lâmina longa."),
         ("Cajado de Fogo", "Arma", 35, "Um cajado que controla o fogo."),
         ("Arco Élfico", "Arma", 28, "Um arco leve feito por elfos."),
         ("Poção de Vida", "Poção", 50, "Recupera pontos de vida."),
         ("Escudo de Ferro", "Armadura", 20, "Um escudo resistente de ferro.")])
    conn.executemany(
        "INSERT INTO magias (nome, nivel, poder, descricao) VALUES (?, ?, ?, ?)",
        [("Faísca", 1, 10, "Uma pequena descarga elétrica."),
         ("Raio Arcano", 2, 20, "Um raio de energia mágica."),
         ("Explosão Mística", 3, 35, "Uma explosão de energia arcana.")])
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
