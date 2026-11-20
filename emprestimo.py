from datetime import date, timedelta

from dados import conectar
from livro import Livro
from usuario import Usuario

PRAZO_PADRAO_DIAS = 14


class Emprestimo:
    def __init__(self, livro, usuario, data_emprestimo, data_devolucao, devolvido=False, id=None):
        self.id = id
        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.devolvido = devolvido

    def esta_atrasado(self):
        if self.devolvido:
            return False
        hoje = str(date.today())
        return hoje > self.data_devolucao

    def dias_para_devolucao(self):
        """Dias até o prazo (negativo = dias de atraso)."""
        prazo = date.fromisoformat(self.data_devolucao)
        return (prazo - date.today()).days

    def situacao_prazo(self):
        if self.devolvido:
            return "Devolvido"
        dias = self.dias_para_devolucao()
        if dias < 0:
            return f"ATRASADO há {-dias} dia(s)"
        if dias == 0:
            return "Vence hoje"
        return f"Faltam {dias} dia(s)"

    def __str__(self):
        status = "Devolvido" if self.devolvido else f"Devolução até {self.data_devolucao}"
        return f"[{self.id}] Livro: {self.livro.titulo} | Usuário: {self.usuario.nome} | Empréstimo: {self.data_emprestimo} | {status}"


SELECT_EMPRESTIMOS = """
    SELECT e.id, e.data_emprestimo, e.data_devolucao, e.devolvido,
           l.id, l.titulo, l.autor, l.ano, l.disponivel,
           u.id, u.nome, u.matricula
    FROM Emprestimos e
    JOIN Livros l ON l.id = e.id_livro
    JOIN Usuarios u ON u.id = e.id_usuario
"""


def _montar_emprestimo(linha):
    (id_emp, data_emp, data_dev, devolvido,
     id_livro, titulo, autor, ano, disponivel,
     id_usuario, nome, matricula) = linha
    livro = Livro(titulo, autor, ano, bool(disponivel), id_livro)
    usuario = Usuario(nome, matricula, id_usuario)
    return Emprestimo(livro, usuario, data_emp, data_dev, bool(devolvido), id_emp)


def _buscar_emprestimos(where="", params=()):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(SELECT_EMPRESTIMOS + where + " ORDER BY e.data_emprestimo, e.id", params)
    emprestimos = [_montar_emprestimo(linha) for linha in cur.fetchall()]
    conn.close()
    return emprestimos


# 1. Registrar empréstimo com prazo de devolução
def registrar_emprestimo(id_livro, id_usuario, prazo_dias=PRAZO_PADRAO_DIAS):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT disponivel FROM Livros WHERE id = ?", (id_livro,))
    livro = cur.fetchone()
    if livro is None:
        conn.close()
        print(f"Livro ID {id_livro} não encontrado.")
        return False
    if not livro[0]:
        conn.close()
        print(f"Livro ID {id_livro} já está emprestado.")
        return False

    cur.execute("SELECT 1 FROM Usuarios WHERE id = ?", (id_usuario,))
    if cur.fetchone() is None:
        conn.close()
        print(f"Usuário ID {id_usuario} não encontrado.")
        return False

    hoje = date.today()
    data_devolucao = hoje + timedelta(days=prazo_dias)
    cur.execute("""
        INSERT INTO Emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao, devolvido)
        VALUES (?, ?, ?, ?, 0)
    """, (id_livro, id_usuario, str(hoje), str(data_devolucao)))
    cur.execute("UPDATE Livros SET disponivel = 0 WHERE id = ?", (id_livro,))
    conn.commit()
    conn.close()
    print(f"Empréstimo registrado! Devolução até {data_devolucao}.")
    return True


# 2. Registrar devolução do livro
def devolver_livro(id_emprestimo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_livro, data_devolucao, devolvido FROM Emprestimos WHERE id = ?", (id_emprestimo,))
    linha = cur.fetchone()
    if linha is None:
        conn.close()
        print(f"Empréstimo ID {id_emprestimo} não encontrado.")
        return False
    id_livro, data_devolucao, devolvido = linha
    if devolvido:
        conn.close()
        print(f"Empréstimo ID {id_emprestimo} já foi devolvido.")
        return False

    cur.execute("UPDATE Emprestimos SET devolvido = 1 WHERE id = ?", (id_emprestimo,))
    cur.execute("UPDATE Livros SET disponivel = 1 WHERE id = ?", (id_livro,))
    conn.commit()
    conn.close()

    dias_atraso = (date.today() - date.fromisoformat(data_devolucao)).days
    if dias_atraso > 0:
        print(f"Livro devolvido com {dias_atraso} dia(s) de atraso.")
    else:
        print("Livro devolvido dentro do prazo.")
    return True


# 3. Renovar o prazo de devolução
def renovar_emprestimo(id_emprestimo, dias_extras=PRAZO_PADRAO_DIAS):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT data_devolucao, devolvido FROM Emprestimos WHERE id = ?", (id_emprestimo,))
    linha = cur.fetchone()
    if linha is None or linha[1]:
        conn.close()
        print(f"Empréstimo ID {id_emprestimo} não encontrado ou já devolvido.")
        return False
    if date.fromisoformat(linha[0]) < date.today():
        conn.close()
        print("Empréstimo atrasado não pode ser renovado. Devolva o livro.")
        return False

    novo_prazo = date.fromisoformat(linha[0]) + timedelta(days=dias_extras)
    cur.execute("UPDATE Emprestimos SET data_devolucao = ? WHERE id = ?", (str(novo_prazo), id_emprestimo))
    conn.commit()
    conn.close()
    print(f"Empréstimo renovado! Nova data de devolução: {novo_prazo}.")
    return True


# 4. Listar livros emprestados (ainda não devolvidos) por um usuário
def listar_livros_emprestados_usuario(id_usuario):
    emprestimos = _buscar_emprestimos("WHERE e.id_usuario = ? AND e.devolvido = 0", (id_usuario,))
    if not emprestimos:
        print(f"O usuário ID {id_usuario} não possui livros emprestados.")
    else:
        print(f"=== Livros emprestados por {emprestimos[0].usuario.nome} ===")
        for emp in emprestimos:
            print(f"{emp.livro} | Devolução até {emp.data_devolucao} | {emp.situacao_prazo()}")
    return emprestimos


# 5. Exibir histórico de empréstimos de um usuário
def historico_emprestimos_usuario(id_usuario):
    emprestimos = _buscar_emprestimos("WHERE e.id_usuario = ?", (id_usuario,))
    if not emprestimos:
        print(f"O usuário ID {id_usuario} não possui histórico de empréstimos.")
    else:
        print(f"=== Histórico de empréstimos de {emprestimos[0].usuario.nome} ===")
        for emp in emprestimos:
            print(f"[{emp.id}] {emp.livro.titulo} | Empréstimo: {emp.data_emprestimo} "
                  f"| Prazo: {emp.data_devolucao} | {emp.situacao_prazo()}")
    return emprestimos


# 6. Controle de prazos: empréstimos atrasados
def listar_emprestimos_atrasados():
    hoje = str(date.today())
    emprestimos = _buscar_emprestimos("WHERE e.devolvido = 0 AND e.data_devolucao < ?", (hoje,))
    if not emprestimos:
        print("Nenhum empréstimo atrasado.")
    else:
        print("=== Empréstimos atrasados ===")
        for emp in emprestimos:
            print(f"{emp} | {emp.situacao_prazo()}")
    return emprestimos


# 7. Controle de prazos: empréstimos que vencem nos próximos dias
def listar_emprestimos_a_vencer(dias=3):
    hoje = date.today()
    limite = hoje + timedelta(days=dias)
    emprestimos = _buscar_emprestimos(
        "WHERE e.devolvido = 0 AND e.data_devolucao >= ? AND e.data_devolucao <= ?",
        (str(hoje), str(limite)),
    )
    if not emprestimos:
        print(f"Nenhum empréstimo vence nos próximos {dias} dia(s).")
    else:
        print(f"=== Empréstimos que vencem nos próximos {dias} dia(s) ===")
        for emp in emprestimos:
            print(f"{emp} | {emp.situacao_prazo()}")
    return emprestimos
