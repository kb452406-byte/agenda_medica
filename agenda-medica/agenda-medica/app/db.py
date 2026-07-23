"""
Camada de acesso ao banco de dados SQLite.

Usamos sqlite3 puro (sem ORM) de propósito: o desafio pede conhecimento
de banco SQL, então é importante deixar as queries explícitas e fáceis
de ler, em vez de escondê-las atrás de um ORM.
"""

import sqlite3

import click
from flask import current_app, g


def get_db():
    """
    Retorna a conexão SQLite da requisição atual.

    O objeto "g" é um espaço de armazenamento do Flask que vive apenas
    durante uma requisição, então a conexão é criada uma única vez por
    requisição e reaproveitada se for chamada mais de uma vez.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # row_factory faz cada linha se comportar como um dicionário,
        # permitindo acessar colunas por nome (ex.: usuario["email"]).
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Fecha a conexão com o banco ao final da requisição, se existir."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    Cria as tabelas necessárias caso ainda não existam.

    Usa "CREATE TABLE IF NOT EXISTS" (ver schema.sql) para ser seguro
    de rodar em toda inicialização da aplicação, sem apagar dados já
    existentes.
    """
    db = get_db()
    with current_app.open_resource("schema.sql") as arquivo_sql:
        db.executescript(arquivo_sql.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Comando de linha de comando: flask init-db"""
    init_db()
    click.echo("Banco de dados inicializado.")


def init_app(app):
    """Registra as funções de banco de dados na aplicação Flask."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
