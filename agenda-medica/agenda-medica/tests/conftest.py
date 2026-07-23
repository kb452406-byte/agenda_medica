"""
Fixtures compartilhadas pelos testes automatizados.

Cada teste roda com uma instância nova da aplicação, apontando para
um arquivo SQLite temporário, para que os testes não interfiram uns
nos outros nem no banco de dados real.
"""

import os
import tempfile

import pytest

from app import create_app
from app import db as db_module
from app.models import criar_usuario

USUARIO_TESTE = "usuario_teste"
SENHA_TESTE = "senha123"


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    aplicacao = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "API_URL": "http://api-inexistente.local/agendamentos",
    })

    with aplicacao.app_context():
        db_module.init_db()
        criar_usuario(USUARIO_TESTE, "teste@agenda.com", SENHA_TESTE)

    yield aplicacao

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, usuario=USUARIO_TESTE, senha=SENHA_TESTE):
    return client.post("/login", data={"usuario": usuario, "senha": senha})
