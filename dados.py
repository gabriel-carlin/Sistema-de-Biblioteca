import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

livros = []
usuarios = []
emprestimos = []

STRING_CONEXAO = (
    f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "TrustServerCertificate=yes;"
)


def conectar():
    return pyodbc.connect(STRING_CONEXAO)