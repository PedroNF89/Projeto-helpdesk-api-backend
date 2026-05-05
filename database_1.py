# =============================================================
#  database.py — Gerenciamento da conexão com o SQLite
#  SQLite é um banco de dados que fica salvo em um único arquivo.
# =============================================================

import sqlite3

# Nome do arquivo onde os dados serão salvos
DATABASE = "tarefas.db"


def get_connection():
    """
    Abre e retorna uma conexão com o banco de dados.
    row_factory faz com que cada linha retorne como dicionário
    (ex: {"id": 1, "titulo": "...", "status": "..."})
    em vez de uma tupla simples (1, "...", "...").
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Cria a tabela 'tarefas' caso ela ainda não exista.
    Chamada uma única vez ao iniciar o servidor.
    """
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT    NOT NULL,
            status TEXT    NOT NULL DEFAULT 'pendente'
        )
        """
    )
    conn.commit()
    conn.close()
