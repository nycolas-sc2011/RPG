"""
personagens.py - Funções da tabela PERSONAGENS.

Colunas: id, nome, nivel, jogador_id, classe_id, energia

jogador_id e classe_id são CHAVES ESTRANGEIRAS: guardam o id de um
jogador e de uma classe. Para mostrar o APELIDO do jogador e o NOME da
classe, junte as tabelas com JOIN.

As consultas (buscar_por_id, buscar_por_nome e listar) devem devolver
as colunas nesta ordem, que é a ordem que o main.py mostra na tela:
    (id, nome, nivel, apelido do jogador, nome da classe)

TAREFA: complete as 4 funções.
"""

# Consulta comum para buscar e listar personagens.
CONSULTA = """
    SELECT personagens.id, personagens.nome, personagens.nivel,
            jogadores.apelido, classes.nome, personagens.energia
    FROM personagens
    JOIN jogadores ON jogadores.id = personagens.jogador_id
    JOIN classes ON classes.id = personagens.classe_id
"""


def incluir(conn, nome, nivel, jogador_id, classe_id, magias_ids=None):
    """Insere um personagem e devolve o id gerado."""
    if nivel < 1 or nivel > 100:
        raise ValueError("O nível do personagem deve ser de 1 a 100.")

    classe = conn.execute(
        "SELECT nome FROM classes WHERE id = ?", (classe_id,)).fetchone()
    eh_feiticeiro = classe is not None and classe[0].strip().casefold() == "feiticeiro"
    magias_ids = magias_ids or []

    if eh_feiticeiro and len(magias_ids) != nivel:
        raise ValueError("Escolha uma magia para cada nível do personagem.")

    if not eh_feiticeiro and magias_ids:
        raise ValueError("Somente feiticeiros podem receber magias.")

    for nivel_personagem, magia_id in enumerate(magias_ids, start=1):
        magia = conn.execute(
            "SELECT nivel FROM magias WHERE id = ?", (magia_id,)).fetchone()
        if magia is None:
            raise ValueError("Uma das magias escolhidas não existe.")
        if magia[0] > nivel_personagem:
            raise ValueError(
                "A magia escolhida precisa ter nível igual ou menor ao nível "
                "do personagem.")

    cursor = conn.execute(
        "INSERT INTO personagens (nome, nivel, jogador_id, classe_id, energia) "
        "VALUES (?, ?, ?, ?, ?)",
        (nome, nivel, jogador_id, classe_id, 50 if eh_feiticeiro else 0))
    personagem_id = cursor.lastrowid

    for nivel_personagem, magia_id in enumerate(magias_ids, start=1):
        conn.execute(
            "INSERT INTO personagem_magias "
            "(personagem_id, magia_id, nivel_personagem) VALUES (?, ?, ?)",
            (personagem_id, magia_id, nivel_personagem))

    conn.commit()
    return personagem_id


def descansar(conn, id):
    """Recupera a energia de um feiticeiro até 100%."""
    personagem = conn.execute(
        "SELECT classes.nome FROM personagens "
        "JOIN classes ON classes.id = personagens.classe_id "
        "WHERE personagens.id = ?", (id,)).fetchone()
    if personagem is None:
        raise ValueError("Personagem não encontrado.")
    if personagem[0].strip().casefold() != "feiticeiro":
        raise ValueError("Somente feiticeiros podem recuperar energia mágica.")
    conn.execute("UPDATE personagens SET energia = 100 WHERE id = ?", (id,))
    conn.commit()


def buscar_por_id(conn, id):
    """Devolve UMA linha, ou None.
    Dica: conn.execute(CONSULTA + " WHERE personagens.id = ?", (id,))"""
    cursor = conn.execute(CONSULTA + " WHERE personagens.id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com os personagens cujo nome contém o texto."""
    cursor = conn.execute(
        CONSULTA + " WHERE personagens.nome LIKE ? ORDER BY personagens.nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todos os personagens."""
    cursor = conn.execute(CONSULTA + " ORDER BY personagens.id")
    return cursor.fetchall()
