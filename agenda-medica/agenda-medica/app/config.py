"""
Configurações da aplicação.

Todos os valores sensíveis (chave secreta, caminho do banco, URL da API)
são lidos de variáveis de ambiente, para que possam ser trocados
facilmente entre ambientes (desenvolvimento, testes, Docker) sem
alterar o código.
"""

import os


class Config:
    # Chave usada pelo Flask para assinar a sessão do usuário.
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-para-desenvolvimento")

    # Caminho do arquivo SQLite. Por padrão fica dentro de "instance/",
    # pasta que o Flask já ignora de versionamento por convenção.
    DATABASE = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.getcwd(), "instance", "agenda_medica.sqlite"),
    )

    # Endereço da API de agendamentos (serviço separado, ver mock_api/).
    API_URL = os.environ.get("API_URL", "http://localhost:5001/agendamentos")

    # Tempo máximo (segundos) que a aplicação espera pela resposta da API.
    API_TIMEOUT = float(os.environ.get("API_TIMEOUT", "5"))
