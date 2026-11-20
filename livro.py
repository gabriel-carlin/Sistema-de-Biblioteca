from dados import conectar

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
        if isinstance(outro, Livro):
            return self.id == outro.id
        return False

# 1. Cadastrar novo livro (INSERT)
def cadastrar_livro(titulo, autor, ano):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Livros (titulo, autor, ano, disponivel)
        VALUES (?, ?, ?, 1)
    """, (titulo, autor, ano))
    conn.commit()
    conn.close()
    print(f"Livro '{titulo}' cadastrado com sucesso no banco de dados!")

# 2. Editar informações de um livro (UPDATE)
def editar_livro(id_livro, novo_titulo=None, novo_autor=None, novo_ano=None):
    conn = conectar()
    cur = conn.cursor()
    
    # Atualiza apenas os campos que foram preenchidos
    if novo_titulo:
        cur.execute("UPDATE Livros SET titulo = ? WHERE id = ?", (novo_titulo, id_livro))
    if novo_autor:
        cur.execute("UPDATE Livros SET autor = ? WHERE id = ?", (novo_autor, id_livro))
    if novo_ano:
        cur.execute("UPDATE Livros SET ano = ? WHERE id = ?", (novo_ano, id_livro))
        
    conn.commit()
    conn.close()
    print(f"Livro ID {id_livro} atualizado com sucesso no banco de dados!")

# 3. Remover um livro (DELETE)
def remover_livro(id_livro):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM Livros WHERE id = ?", (id_livro,))
    conn.commit()
    conn.close()
    print(f"Livro ID {id_livro} removido com sucesso do banco de dados!")

# 4. Listar livros cadastrados (SELECT)
def listar_livros():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, autor, ano, disponivel FROM Livros ORDER BY titulo")
    livros = [
        Livro(titulo, autor, ano, bool(disponivel), id)
        for id, titulo, autor, ano, disponivel in cur.fetchall()
    ]
    conn.close()

    if not livros:
        print("Nenhum livro cadastrado.")
    else:
        print("=== Livros cadastrados ===")
        for livro in livros:
            print(livro)
    return livros
