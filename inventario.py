"""
inventario.py - Funções da tabela INVENTARIO.   (DESAFIO)

Colunas: id, personagem_id, item_id, quantidade

Cada linha do inventário diz que um PERSONAGEM carrega um ITEM, em uma
certa quantidade. A busca "por nome" deve procurar pelo nome do PERSONAGEM.

As consultas devem devolver as colunas nesta ordem:
    (id, nome do personagem, nome do item, tipo, descrição, quantidade)

TAREFA: escreva a CONSULTA (com dois JOINs) e complete as 4 funções.
Dica: o arquivo personagens.py faz algo muito parecido.
"""

CONSULTA = """
        SELECT inventario.id, personagens.nome, itens.nome, itens.tipo,
            itens.descricao, inventario.quantidade
    FROM inventario
    JOIN personagens ON personagens.id = inventario.personagem_id
    JOIN itens ON itens.id = inventario.item_id
"""


def incluir(conn, personagem_id, item_id, quantidade):
    """Coloca um item no inventário de um personagem e devolve o id gerado."""
    personagem = conn.execute(
        "SELECT classe_id FROM personagens WHERE id = ?", (personagem_id,))
    personagem = personagem.fetchone()
    item = conn.execute("SELECT tipo FROM itens WHERE id = ?", (item_id,))
    item = item.fetchone()

    if personagem is not None and item is not None:
        regra = conn.execute(
            "SELECT classe_id FROM restricoes_tipos WHERE tipo = ?", (item[0],))
        regra = regra.fetchone()
        if regra is not None and personagem[0] != regra[0]:
            classe = conn.execute(
                "SELECT nome FROM classes WHERE id = ?", (regra[0],))
            classe = classe.fetchone()
            raise ValueError(
                "Este tipo de item só pode ser usado pela classe "
                + classe[0] + ".")

    cursor = conn.execute(
        "INSERT INTO inventario (personagem_id, item_id, quantidade) VALUES (?, ?, ?)",
        (personagem_id, item_id, quantidade))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha, ou None."""
    cursor = conn.execute(CONSULTA + " WHERE inventario.id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome_personagem):
    """Devolve uma LISTA com os itens dos personagens cujo nome contém o texto."""
    cursor = conn.execute(
        CONSULTA + " WHERE personagens.nome LIKE ? ORDER BY personagens.nome",
        ("%" + nome_personagem + "%",))
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todo o inventário."""
    cursor = conn.execute(CONSULTA + " ORDER BY inventario.id")
    return cursor.fetchall()
