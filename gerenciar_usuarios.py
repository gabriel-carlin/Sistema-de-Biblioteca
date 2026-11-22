import dados
from usuario import Usuario


def cadastrar_usuario(nome, matricula):
    nome = nome.strip()
    matricula = matricula.strip()

    if not nome or len(nome) > 100:
        raise ValueError("O nome é obrigatório e deve ter no máximo 100 caracteres.")
    if not matricula or len(matricula) > 50:
        raise ValueError("A matrícula é obrigatória e deve ter no máximo 50 caracteres.")

    conexao = dados.conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM Usuarios WHERE matricula = ?", matricula)
        if cursor.fetchone():
            raise ValueError("Já existe um usuário cadastrado com essa matrícula.")

        cursor.execute(
            "INSERT INTO Usuarios (nome, matricula) OUTPUT INSERTED.id VALUES (?, ?)",
            nome,
            matricula,
        )
        novo_id = cursor.fetchone()[0]
        conexao.commit()
    finally:
        conexao.close()

    usuario = Usuario(nome, matricula, novo_id)
    dados.usuarios.append(usuario)
    return usuario


def listar_usuarios():
    conexao = dados.conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, matricula FROM Usuarios ORDER BY nome")
        registros = cursor.fetchall()
    finally:
        conexao.close()

    dados.usuarios[:] = [Usuario(r.nome, r.matricula, r.id) for r in registros]
    return dados.usuarios


def menu_cadastrar_usuario():
    print("\n--- Cadastrar Usuário ---")
    nome = input("Nome: ")
    matricula = input("Matrícula: ")
    try:
        usuario = cadastrar_usuario(nome, matricula)
        print(f"Usuário cadastrado com sucesso: {usuario}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def menu_listar_usuarios():
    print("\n--- Usuários Cadastrados ---")
    usuarios = listar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(usuario)
