"""
API simulada de agendamentos médicos.

Este é um serviço Flask separado e independente da aplicação principal:
ele representa o sistema externo que, em um cenário real, forneceria
os dados de agendamentos. A aplicação principal fala com ele apenas
por HTTP (nunca importa código deste serviço diretamente).

Variável de ambiente SIMULAR_FALHA=1 faz este serviço responder com
erro 503, útil para testar manualmente como a aplicação principal
se comporta quando a API está indisponível.
"""

import os

from flask import Flask, jsonify

app = Flask(__name__)

AGENDAMENTOS = [
    {
        "paciente": "Maria Silva",
        "cpf": "111.111.111-11",
        "medico": "Dr. João Souza",
        "especialidade": "Cardiologia",
        "data": "2026-07-23",
        "horario": "09:00",
        "convenio": "Unimed",
        "status": "Confirmado",
    },
    {
        "paciente": "Carlos Pereira",
        "cpf": "222.222.222-22",
        "medico": "Dra. Ana Lima",
        "especialidade": "Dermatologia",
        "data": "2026-07-23",
        "horario": "10:30",
        "convenio": "Bradesco Saúde",
        "status": "Confirmado",
    },
    {
        "paciente": "Fernanda Costa",
        "cpf": "333.333.333-33",
        "medico": "Dr. João Souza",
        "especialidade": "Cardiologia",
        "data": "2026-07-24",
        "horario": "08:00",
        "convenio": "Particular",
        "status": "Pendente",
    },
    {
        "paciente": "Roberto Alves",
        "cpf": "444.444.444-44",
        "medico": "Dra. Beatriz Nunes",
        "especialidade": "Ortopedia",
        "data": "2026-07-24",
        "horario": "14:15",
        "convenio": "SulAmérica",
        "status": "Cancelado",
    },
    {
        "paciente": "Juliana Ramos",
        "cpf": "555.555.555-55",
        "medico": "Dra. Ana Lima",
        "especialidade": "Dermatologia",
        "data": "2026-07-25",
        "horario": "11:00",
        "convenio": "Unimed",
        "status": "Confirmado",
    },
    {
        "paciente": "Pedro Martins",
        "cpf": "666.666.666-66",
        "medico": "Dra. Beatriz Nunes",
        "especialidade": "Ortopedia",
        "data": "2026-07-25",
        "horario": "16:45",
        "convenio": "Particular",
        "status": "Confirmado",
    },
]


@app.route("/agendamentos")
def agendamentos():
    if os.environ.get("SIMULAR_FALHA") == "1":
        return jsonify({"erro": "Serviço temporariamente indisponível"}), 503

    return jsonify(AGENDAMENTOS)


@app.route("/")
def raiz():
    return jsonify({"status": "ok", "mensagem": "Mock API de agendamentos"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
