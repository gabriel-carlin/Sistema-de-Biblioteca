class Usuario:
    def __init__(self, nome, matricula, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula

    def __str__(self):
        return f"[{self.id}] {self.nome} (Matrícula: {self.matricula})"

    def __eq__(self, outro):
        return self.id == outro.id