"""
Cliente responsável por buscar os agendamentos na API externa.

Toda a integração HTTP fica concentrada neste módulo. As rotas nunca
chamam "requests" diretamente: elas chamam "buscar_agendamentos()" e
tratam apenas a exceção "ErroAPIAgendamentos", o que mantém o
tratamento de erros consistente em toda a aplicação.
"""

import requests
from flask import current_app

# Campos que a aplicação exige em cada agendamento retornado pela API.
CAMPOS_OBRIGATORIOS = [
    "paciente",
    "cpf",
    "medico",
    "especialidade",
    "data",
    "horario",
    "convenio",
    "status",
]


class ErroAPIAgendamentos(Exception):
    """
    Erro genérico de comunicação com a API de agendamentos.

    A mensagem já vem pronta para ser exibida ao usuário final,
    então as rotas não precisam interpretar o tipo de exceção.
    """


def buscar_agendamentos():
    """
    Faz a requisição HTTP para a API de agendamentos e devolve uma
    lista de dicionários já validados.

    Cobre os cenários pedidos no desafio:
      - indisponibilidade temporária da API (conexão recusada/timeout);
      - resposta vazia ou inválida (JSON malformado);
      - campos obrigatórios ausentes na resposta (registros incompletos
        são descartados, sem derrubar a aplicação).
    """
    url = current_app.config["API_URL"]
    timeout = current_app.config["API_TIMEOUT"]

    try:
        resposta = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError as exc:
        raise ErroAPIAgendamentos(
            "Não foi possível conectar à API de agendamentos. "
            "Verifique se o serviço está disponível."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise ErroAPIAgendamentos(
            "A API de agendamentos demorou demais para responder."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ErroAPIAgendamentos(
            f"Erro inesperado ao chamar a API de agendamentos: {exc}"
        ) from exc

    if resposta.status_code != 200:
        raise ErroAPIAgendamentos(
            f"A API de agendamentos retornou um erro (status {resposta.status_code})."
        )

    try:
        dados = resposta.json()
    except ValueError as exc:
        raise ErroAPIAgendamentos(
            "A API de agendamentos retornou uma resposta inválida (JSON malformado)."
        ) from exc

    # Resposta vazia é tratada como "nenhum agendamento", não como erro.
    if dados is None:
        return []

    if not isinstance(dados, list):
        raise ErroAPIAgendamentos(
            "Formato de resposta inesperado da API de agendamentos."
        )

    return _filtrar_registros_validos(dados)


def _filtrar_registros_validos(registros):
    """
    Mantém apenas os agendamentos que possuem todos os campos
    obrigatórios preenchidos. Registros incompletos são descartados
    silenciosamente, para não quebrar a exibição da tabela por causa
    de um único registro malformado vindo da API.
    """
    validos = []
    for item in registros:
        if not isinstance(item, dict):
            continue

        campos_ausentes = [
            campo for campo in CAMPOS_OBRIGATORIOS
            if not item.get(campo)
        ]
        if campos_ausentes:
            continue

        validos.append(item)

    return validos
