# 📚 Sistema de Biblioteca

Projeto simples em Python para gerenciamento de livros e empréstimos, utilizando apenas dados em memória (com opção de persistência em disco).

---

## Entidades Principais

* **📖 Livro**
  * `título`
  * `autor`
  * `ano`
  * `disponível`
* **👤 Usuário**
  * `nome`
  * `matrícula`
* **📑 Empréstimo**
  * `livro`
  * `usuário`
  * `data do empréstimo`
  * `data de devolução`

---

## ✅ Funcionalidades Obrigatórias

* Listar livros cadastrados
* Cadastrar novo livro
* Editar informações de um livro
* Remover livro
* Cadastrar usuários
* Listar usuários cadastrados
* Listar livros emprestados por um usuário
* Realizar empréstimo de livro
* Devolver livro
* Bloquear empréstimo se o livro não estiver disponível

---

## ✨ Funcionalidades Adicionais (Opcional / Ponto Bônus)

* Exibir histórico de empréstimos por usuário
* Controlar prazo de devolução dos livros
* Gravar em disco

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** — Linguagem principal
* **Bibliotecas nativas apenas** (sem dependências externas)

---

## 🎓 Avaliação

* **Funcionalidades obrigatórias:** Nota base
* **Funcionalidades adicionais:** Ponto bônus
* **Requisitos obrigatórios não atendidos:** Ponto negativo
* **Observação:** Qualidade e clareza do código também serão avaliadas.

---

## 💡Dicas de Implementação

* Use **listas** para armazenar dados em memória.
* Utilize **classes** para representar entidades (`Livro`, `Usuário`, `Empréstimo`).
* Use **loops e condicionais** para implementar o menu de opções.