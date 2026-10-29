"""Funções para cadastrar e usar magias."""


def incluir(conn, nome, nivel, poder, descricao):
    """Cria uma magia e devolve o id gerado."""
    if nivel < 1 or nivel > 100:
        raise ValueError("O nível da magia deve ser de 1 a 100.")
    if poder < 0:
        raise ValueError("O dano não pode ser negativo.")

    cursor = conn.execute(
        "INSERT INTO magias (nome, nivel, poder, descricao) VALUES (?, ?, ?, ?)",
        (nome, nivel, poder, descricao))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Busca uma magia pelo id."""
    cursor = conn.execute(
        "SELECT id, nome, nivel, poder, descricao FROM magias WHERE id = ?",
        (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Busca magias pelo nome ou parte dele."""
    cursor = conn.execute(
        "SELECT id, nome, nivel, poder, descricao FROM magias "
        "WHERE nome LIKE ? ORDER BY nivel, nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    """Lista todas as magias."""
    cursor = conn.execute(
        "SELECT id, nome, nivel, poder, descricao FROM magias ORDER BY nivel, nome")
    return cursor.fetchall()


def alterar_nome(conn, id, nome_novo):
    """Atualiza o nome de uma magia existente."""
    nome_novo = nome_novo.strip()
    if nome_novo == "":
        raise ValueError("O nome da magia não pode ficar vazio.")

    cursor = conn.execute(
        "UPDATE magias SET nome = ? WHERE id = ?",
        (nome_novo, id))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError("Nenhuma magia com esse id foi encontrada.")
    return id


def listar_ate_nivel(conn, nivel):
    """Lista magias que o personagem já pode aprender nesse nível."""
    cursor = conn.execute(
        "SELECT id, nome, nivel, poder, descricao FROM magias "
        "WHERE nivel <= ? ORDER BY nivel, nome",
        (nivel,))
    return cursor.fetchall()


def listar_do_personagem(conn, personagem_id):
    """Lista as magias aprendidas por um personagem."""
    cursor = conn.execute(
        "SELECT magias.id, magias.nome, magias.nivel, magias.poder, "
        "magias.descricao, personagem_magias.nivel_personagem "
        "FROM personagem_magias "
        "JOIN magias ON magias.id = personagem_magias.magia_id "
        "WHERE personagem_magias.personagem_id = ? "
        "ORDER BY personagem_magias.nivel_personagem",
        (personagem_id,))
    return cursor.fetchall()


def custo_energia(nivel):
    """Calcula o custo de energia usando o nível da magia."""
    if nivel < 1 or nivel > 100:
        raise ValueError("O nível da magia deve ser de 1 a 100.")
    if nivel <= 20:
        return 1
    if nivel <= 50:
        return 2
    if nivel <= 80:
        return 3
    return 4


def conjurar(conn, personagem_id, magia_id):
    """Usa uma magia aprendida e desconta a energia necessária."""
    personagem = conn.execute(
        "SELECT classes.nome, personagens.energia FROM personagens "
        "JOIN classes ON classes.id = personagens.classe_id "
        "WHERE personagens.id = ?", (personagem_id,)).fetchone()
    if personagem is None:
        raise ValueError("Personagem não encontrado.")
    if personagem[0].strip().casefold() != "feiticeiro":
        raise ValueError("Somente feiticeiros podem conjurar magias.")

    magia = conn.execute(
        "SELECT magias.nome, magias.nivel, magias.poder, magias.descricao "
        "FROM personagem_magias "
        "JOIN magias ON magias.id = personagem_magias.magia_id "
        "WHERE personagem_magias.personagem_id = ? AND magias.id = ?",
        (personagem_id, magia_id)).fetchone()
    if magia is None:
        raise ValueError("Esse personagem não aprendeu essa magia.")

    custo = custo_energia(magia[1])
    energia = personagem[1]
    if energia < custo:
        raise ValueError("Energia insuficiente para conjurar essa magia.")

    energia -= custo
    conn.execute(
        "UPDATE personagens SET energia = ? WHERE id = ?",
        (energia, personagem_id))
    conn.commit()
    return magia[0], magia[2], custo, energia