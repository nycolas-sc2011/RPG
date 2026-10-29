"""
main.py - Programa principal do jogo de RPG.

Abre a conexão com o banco, mostra o menu e chama as funções
de cada tabela (classes.py, jogadores.py, itens.py, personagens.py
e inventario.py).

Para rodar:  python main.py
"""

import sqlite3

import banco
import classes
import jogadores
import itens
import personagens
import inventario
import magias


# Funções de apoio: ler números do teclado e mostrar tabelas na tela

def ler_inteiro(mensagem):
    """Pergunta até o usuário digitar um número inteiro."""
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print("  Digite um número inteiro.")


def ler_nivel(mensagem):
    """Lê um nível entre 1 e 100."""
    while True:
        nivel = ler_inteiro(mensagem)
        if 1 <= nivel <= 100:
            return nivel
        print("  O nível deve ser de 1 a 100.")


def ler_texto(mensagem):
    """Pergunta até o usuário digitar algum texto (não aceita vazio)."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("  Este campo não pode ficar vazio.")


def mostrar(colunas, linhas):
    """Mostra uma lista de linhas como uma tabela com cabeçalho."""
    if not linhas:
        print("  Nenhum registro encontrado.")
        return
    # largura de cada coluna = maior texto daquela coluna
    larguras = []
    for i, nome in enumerate(colunas):
        maior = max(len(str(linha[i])) for linha in linhas)
        larguras.append(max(len(nome), maior))
    print("  " + " | ".join(nome.ljust(l) for nome, l in zip(colunas, larguras)))
    print("  " + "-+-".join("-" * l for l in larguras))
    for linha in linhas:
        print("  " + " | ".join(str(v).ljust(l) for v, l in zip(linha, larguras)))


# Perguntas para incluir um registro em cada tabela.
# Cada função devolve os valores na ordem dos parâmetros de incluir().

def dados_classe():
    nome = ler_texto("Nome da classe: ")
    return (nome,)


def dados_jogador():
    nome = ler_texto("Nome do jogador: ")
    apelido = input("Apelido (nick): ").strip()
    return (nome, apelido)


def dados_item():
    nome = ler_texto("Nome do item: ")
    tipo = input("Tipo (Arma, Poção, Armadura...): ").strip()
    poder = ler_inteiro("Poder: ")
    descricao = input("Descrição: ").strip()
    return (nome, tipo, poder, descricao)


def dados_magia():
    nome = ler_texto("Nome da magia: ")
    nivel = ler_nivel("Nível da magia (1 a 100): ")
    poder = ler_inteiro("Dano: ")
    descricao = input("Descrição: ").strip()
    return (nome, nivel, poder, descricao)


def dados_personagem(conn):
    nome = ler_texto("Nome do personagem: ")
    nivel = ler_nivel("Nível (1 a 100): ")
    jogador_id = ler_inteiro("Id do jogador: ")
    classe_id = ler_inteiro("Id da classe: ")
    magias_ids = []

    classe = classes.buscar_por_id(conn, classe_id)
    if classe is not None and classe[1].strip().casefold() == "feiticeiro":
        for nivel_personagem in range(1, nivel + 1):
            disponiveis = magias.listar_ate_nivel(conn, nivel_personagem)
            if not disponiveis:
                raise ValueError(
                    "Cadastre primeiro uma magia de nível "
                    + str(nivel_personagem) + " ou menor.")

            print("Magia para o nível do personagem", nivel_personagem)
            mostrar(["Id", "Nome", "Nível", "Dano", "Descrição"], disponiveis)
            magia_id = ler_inteiro("Id da magia: ")
            while not any(magia[0] == magia_id for magia in disponiveis):
                print("  Escolha uma magia da lista.")
                magia_id = ler_inteiro("Id da magia: ")
            magias_ids.append(magia_id)

    return (nome, nivel, jogador_id, classe_id, magias_ids)


def dados_inventario():
    personagem_id = ler_inteiro("Id do personagem: ")
    item_id = ler_inteiro("Id do item: ")
    quantidade = ler_inteiro("Quantidade: ")
    return (personagem_id, item_id, quantidade)


# ------------------------------------------------------------------
# Cada tabela do menu: título, módulo com as funções, nomes das colunas
# que aparecem na tela e a função que pergunta os dados para incluir.
# ------------------------------------------------------------------

TABELAS = {
    "1": ("Classes",     classes,     ["Id", "Nome"],                                     dados_classe),
    "2": ("Jogadores",   jogadores,   ["Id", "Nome", "Apelido"],                          dados_jogador),
    "3": ("Itens",       itens,       ["Id", "Nome", "Tipo", "Poder", "Descrição"],      dados_item),
    "4": ("Personagens", personagens, ["Id", "Nome", "Nível", "Jogador", "Classe", "Energia (%)"], dados_personagem),
    "5": ("Inventário",  inventario,  ["Id", "Personagem", "Item", "Tipo", "Descrição", "Quantidade"], dados_inventario),
    "6": ("Magias",      magias,      ["Id", "Nome", "Nível", "Dano", "Descrição"],       dados_magia),
}


def submenu(conn, titulo, modulo, colunas, pedir_dados):
    """Menu de uma tabela: incluir, buscar por id, buscar por nome, listar."""
    while True:
        print(f"\n--- {titulo.upper()} ---")
        print("1 - Incluir")
        print("2 - Buscar por id")
        print("3 - Buscar por nome")
        print("4 - Listar todos")
        if modulo is itens:
            print("5 - Buscar por tipo")
            print("6 - Configurar classe permitida por tipo")
        if modulo is magias:
            print("5 - Alterar nome")
        if modulo is personagens:
            print("6 - Conjurar magia")
            print("7 - Descansar e recuperar energia")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                if modulo is personagens:
                    valores = dados_personagem(conn)
                else:
                    valores = pedir_dados()
                novo_id = modulo.incluir(conn, *valores)   # * "espalha" a tupla nos parâmetros
                print(f"  Registro incluído com id {novo_id}.")
            elif opcao == "2":
                id = ler_inteiro("Id: ")
                linha = modulo.buscar_por_id(conn, id)
                if linha is None:
                    print("  Nenhum registro com esse id.")
                else:
                    mostrar(colunas, [linha])
            elif opcao == "3":
                texto = ler_texto("Nome (ou parte dele): ")
                mostrar(colunas, modulo.buscar_por_nome(conn, texto))
            elif opcao == "4":
                mostrar(colunas, modulo.listar(conn))
            elif opcao == "5" and modulo is itens:
                tipo = ler_texto("Tipo (ou parte dele): ")
                mostrar(colunas, itens.buscar_por_tipo(conn, tipo))
            elif opcao == "5" and modulo is magias:
                magia_id = ler_inteiro("Id da magia: ")
                nome_novo = ler_texto("Novo nome da magia: ")
                magias.alterar_nome(conn, magia_id, nome_novo)
                print("  Nome da magia atualizado.")
            elif opcao == "6" and modulo is itens:
                tipo = ler_texto("Tipo do item: ")
                print("Classes disponíveis:")
                mostrar(["Id", "Classe"], classes.listar(conn))
                classe_id = ler_inteiro(
                    "Id da classe permitida (0 para remover a regra): ")
                if classe_id == 0:
                    itens.remover_classe_do_tipo(conn, tipo)
                    print("  Restrição removida para esse tipo.")
                else:
                    itens.definir_classe_do_tipo(conn, tipo, classe_id)
                    print("  Classe permitida configurada.")
            elif opcao == "6" and modulo is personagens:
                personagem_id = ler_inteiro("Id do feiticeiro: ")
                conhecidas = magias.listar_do_personagem(conn, personagem_id)
                mostrar(
                    ["Id", "Magia", "Nível", "Dano", "Descrição", "Nível do personagem"],
                    conhecidas)
                magia_id = ler_inteiro("Id da magia para conjurar: ")
                nome, dano, custo, energia = magias.conjurar(
                    conn, personagem_id, magia_id)
                print(f"  {nome} causou {dano} de dano.")
                print(f"  Energia gasta: {custo}. Energia restante: {energia}%.")
            elif opcao == "7" and modulo is personagens:
                personagem_id = ler_inteiro("Id do feiticeiro: ")
                personagens.descansar(conn, personagem_id)
                print("  Energia recuperada para 100%.")
            elif opcao == "0":
                return
            else:
                print("  Opção inválida.")
        except NotImplementedError:
            print("  Esta função ainda não foi implementada. Abra o arquivo "
                  f"{modulo.__name__}.py e complete o código.")
        except ValueError as erro:
            print(f"  {erro}")
        except sqlite3.IntegrityError as erro:
            print(f"  O banco recusou a operação: {erro}")
            print("  (Confira se os ids informados existem.)")


def main():
    conn = banco.conectar()          # abre o arquivo rpg.db
    print("Conectado ao banco:", banco.NOME_ARQUIVO)

    while True:
        print("\n===== RPG - CADASTRO DO JOGO =====")
        for chave, (titulo, *_) in TABELAS.items():
            print(f"{chave} - {titulo}")
        print("7 - Carregar dados de exemplo")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao in TABELAS:
            titulo, modulo, colunas, pedir_dados = TABELAS[opcao]
            submenu(conn, titulo, modulo, colunas, pedir_dados)
        elif opcao == "7":
            if banco.carregar_exemplos(conn):
                print("  Dados de exemplo carregados.")
            else:
                print("  O banco já tem dados; nada foi alterado.")
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")

    conn.close()                     # fecha a conexão antes de sair
    print("Até logo!")


if __name__ == "__main__":
    main()
