from datetime import date


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

    def __str__(self):
        status = "Devolvido" if self.devolvido else f"Devolução até {self.data_devolucao}"
        return f"[{self.id}] Livro: {self.livro.titulo} | Usuário: {self.usuario.nome} | Empréstimo: {self.data_emprestimo} | {status}"