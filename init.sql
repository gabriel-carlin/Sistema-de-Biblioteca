IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BibliotecaDB')
BEGIN
    CREATE DATABASE BibliotecaDB;
END
GO

USE BibliotecaDB;
GO

IF OBJECT_ID('Livros', 'U') IS NULL
BEGIN
    CREATE TABLE Livros (
        id INT IDENTITY(1,1) PRIMARY KEY,
        titulo VARCHAR(150) NOT NULL,
        autor VARCHAR(100) NOT NULL,
        ano INT NOT NULL,
        disponivel BIT NOT NULL DEFAULT 1
    );
END
GO

IF OBJECT_ID('Usuarios', 'U') IS NULL
BEGIN
    CREATE TABLE Usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        matricula VARCHAR(50) NOT NULL UNIQUE
    );
END
GO

IF OBJECT_ID('Emprestimos', 'U') IS NULL
BEGIN
    CREATE TABLE Emprestimos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_livro INT NOT NULL,
        id_usuario INT NOT NULL,
        data_emprestimo VARCHAR(10) NOT NULL,
        data_devolucao VARCHAR(10) NOT NULL,
        devolvido BIT NOT NULL DEFAULT 0,
        FOREIGN KEY (id_livro) REFERENCES Livros(id),
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
    );
END
GO