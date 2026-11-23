from livro import buscar_livros, cadastrar_livro, listar_livros
from gerenciar_usuarios import listar_usuarios, menu_cadastrar_usuario, menu_listar_usuarios
from emprestimo import (
    PRAZO_PADRAO_DIAS,
    registrar_emprestimo,
    devolver_livro,
    renovar_emprestimo,
    listar_emprestimos_ativos,
    listar_livros_emprestados_usuario,
    historico_emprestimos_usuario,
    listar_emprestimos_atrasados,
    listar_emprestimos_a_vencer,
)


def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número válido.")


def selecionar_id(registros, titulo, campo, mensagem_vazia, exibir=str):
    if not registros:
        print(mensagem_vazia)
        return None

    print(f"=== {titulo} ===")
    for registro in registros:
        print(exibir(registro))
    ids = {registro.id for registro in registros}
    while True:
        escolhido = ler_int(f"ID {campo} [0 para voltar]: ")
        if escolhido == 0:
            return None
        if escolhido in ids:
            return escolhido
        print("Escolha um ID da lista ou digite 0 para voltar.")


def selecionar_usuario():
    return selecionar_id(
        listar_usuarios(), "Usuários cadastrados", "do usuário", "Nenhum usuário cadastrado."
    )


def menu_emprestar():
    id_livro = selecionar_id(
        buscar_livros(apenas_disponiveis=True),
        "Livros disponíveis", "do livro", "Nenhum livro disponível para empréstimo.",
    )
    if id_livro is None:
        return
    id_usuario = selecionar_usuario()
    if id_usuario is None:
        return
    prazo = input(f"Prazo em dias [{PRAZO_PADRAO_DIAS}]: ").strip()
    registrar_emprestimo(id_livro, id_usuario, int(prazo) if prazo else PRAZO_PADRAO_DIAS)


def selecionar_emprestimo():
    return selecionar_id(
        listar_emprestimos_ativos(),
        "Empréstimos ativos", "do empréstimo", "Nenhum empréstimo ativo.",
        exibir=lambda emprestimo: f"{emprestimo} | {emprestimo.situacao_prazo()}",
    )


MENU = """
===== Sistema de Biblioteca =====
1  - Cadastrar livro
2  - Listar livros cadastrados
3  - Cadastrar usuário
4  - Listar usuários
5  - Registrar empréstimo
6  - Devolver livro
7  - Renovar empréstimo
8  - Listar livros emprestados por um usuário
9  - Histórico de empréstimos de um usuário
10 - Empréstimos atrasados
11 - Empréstimos que vencem nos próximos dias
0  - Sair
"""


def main():
    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                cadastrar_livro(input("Título: "), input("Autor: "), ler_int("Ano: "))
            elif opcao == "2":
                listar_livros()
            elif opcao == "3":
                menu_cadastrar_usuario()
            elif opcao == "4":
                menu_listar_usuarios()
            elif opcao == "5":
                menu_emprestar()
            elif opcao in ("6", "7"):
                id_emprestimo = selecionar_emprestimo()
                if id_emprestimo is not None:
                    operacao = devolver_livro if opcao == "6" else renovar_emprestimo
                    operacao(id_emprestimo)
            elif opcao in ("8", "9"):
                id_usuario = selecionar_usuario()
                if id_usuario is not None:
                    consulta = listar_livros_emprestados_usuario if opcao == "8" else historico_emprestimos_usuario
                    consulta(id_usuario)
            elif opcao == "10":
                listar_emprestimos_atrasados()
            elif opcao == "11":
                dias = input("Próximos quantos dias? [3]: ").strip()
                listar_emprestimos_a_vencer(int(dias) if dias else 3)
            elif opcao == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")
        except Exception as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
