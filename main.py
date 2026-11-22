from livro import cadastrar_livro, listar_livros
from gerenciar_usuarios import menu_cadastrar_usuario, menu_listar_usuarios
from emprestimo import (
    registrar_emprestimo,
    devolver_livro,
    renovar_emprestimo,
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
                id_livro = ler_int("ID do livro: ")
                id_usuario = ler_int("ID do usuário: ")
                prazo = input("Prazo em dias [14]: ").strip()
                registrar_emprestimo(id_livro, id_usuario, int(prazo) if prazo else 14)
            elif opcao == "6":
                devolver_livro(ler_int("ID do empréstimo: "))
            elif opcao == "7":
                renovar_emprestimo(ler_int("ID do empréstimo: "))
            elif opcao == "8":
                listar_livros_emprestados_usuario(ler_int("ID do usuário: "))
            elif opcao == "9":
                historico_emprestimos_usuario(ler_int("ID do usuário: "))
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
