"""
Configurações da aplicação.

Todos os valores sensíveis (chave secreta, caminho do banco, URL da API)
são lidos de variáveis de ambiente, para que possam ser trocados
facilmente entre ambientes (desenvolvimento, testes, Docker) sem
alterar o código.
"""

import os


class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-para-desenvolvimento")

    # Caminho do arquivo SQL
    # pasta que o Flask 
    DATABASE = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.getcwd(), "instance", "agenda_medica.sqlite"),
    )

    # Endereço da API de agendamentos 
    API_URL = os.environ.get("API_URL", "http://localhost:5001/agendamentos")

    # Tempo máximo 
    API_TIMEOUT = float(os.environ.get("API_TIMEOUT", "5"))
