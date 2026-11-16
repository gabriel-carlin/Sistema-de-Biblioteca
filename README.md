# Sistema de Biblioteca

Projeto em Python para gerenciamento de livros, usuários e empréstimos com persistência em banco de dados **Microsoft SQL Server (MSSQL)** via Docker.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado na sua máquina:

1. **Python 3**
2. **Docker Desktop** (aberto e em execução)
3. **ODBC Driver 17 (ou 18) for SQL Server** (driver da Microsoft para conexão com o banco)

## Passo a Passo para Rodar o Projeto

### 1. Configurar as variáveis de ambiente (`.env`)

Na raiz do projeto, faça uma cópia do arquivo `.env.example` e renomeie para `.env` (ou rode no terminal):

```bash
cp .env.example .env
```

Abra o seu arquivo `.env` e preencha uma senha de sua escolha em `DB_PASSWORD`:

```env
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=localhost,1433
DB_NAME=BibliotecaDB
DB_USER=sa
DB_PASSWORD=
```

### 2. Subir o banco de dados no Docker

Com o Docker Desktop aberto, execute na pasta raiz do projeto:

```bash
docker compose up -d
```

### 3. Criar o ambiente virtual e instalar dependências

No terminal Git Bash dentro da pasta do projeto, crie e ative a `.venv`:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Com o prefixo `(.venv)` ativo no terminal, instale as bibliotecas do projeto:

```bash
pip install -r requirements.txt
```

### 4. Testar a conexão

Rode o comando abaixo para confirmar que o Python conectou ao banco e encontrou as tabelas:

```bash
python -c "from dados import conectar; conn = conectar(); cur = conn.cursor(); cur.execute('SELECT name FROM sys.tables'); print([r[0] for r in cur.fetchall()]); conn.close()"
```

Saída esperada:

```text
['Livros', 'Usuarios', 'Emprestimos']
```

## Estrutura Base do Projeto

* **`livro.py`**: Classe `Livro(titulo, autor, ano, disponivel=True, id=None)`
* **`usuario.py`**: Classe `Usuario(nome, matricula, id=None)`
* **`emprestimo.py`**: Classe `Emprestimo(livro, usuario, data_emprestimo, data_devolucao, devolvido=False, id=None)` — possui o método `esta_atrasado()`.
* **`dados.py`**: Contém as listas em memória (`livros`, `usuarios`, `emprestimos`) e a função `conectar()`.

## Estrutura das Tabelas (`BibliotecaDB`)

* **`Livros`**: `id` (INT, PK), `titulo` (VARCHAR), `autor` (VARCHAR), `ano` (INT), `disponivel` (BIT)
* **`Usuarios`**: `id` (INT, PK), `nome` (VARCHAR), `matricula` (VARCHAR, UNIQUE)
* **`Emprestimos`**: `id` (INT, PK), `id_livro` (INT, FK), `id_usuario` (INT, FK), `data_emprestimo` (VARCHAR `AAAA-MM-DD`), `data_devolucao` (VARCHAR `AAAA-MM-DD`), `devolvido` (BIT)
