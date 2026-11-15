class Livro:
    def __init__(self, titulo, autor, ano, disponivel=True, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.id}] {self.titulo} - {self.autor} ({self.ano}) [{status}]"

    def __eq__(self, outro):
            return self.id == outro.id