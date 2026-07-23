"""
Script de seed (carga inicial de dados).

Cria um usuário de teste para que a aplicação possa ser usada
imediatamente após subir, sem precisar cadastrar nada manualmente
(requisito 3 da Parte 1: "script, migration ou seed").
"""

import sqlite3

from .models import buscar_usuario_por_login, criar_usuario

USUARIO_TESTE = "medico"
EMAIL_TESTE = "medico@agenda.com"
SENHA_TESTE = "123456"


def seed_test_user():
    """Cria o usuário de teste apenas se ele ainda não existir."""
    if buscar_usuario_por_login(USUARIO_TESTE) is not None:
        return

    try:
        criar_usuario(USUARIO_TESTE, EMAIL_TESTE, SENHA_TESTE)
    except sqlite3.IntegrityError:
        # Corrida entre processos tentando criar o mesmo usuário ao
        # mesmo tempo: não é um erro grave, apenas ignoramos.
        pass
