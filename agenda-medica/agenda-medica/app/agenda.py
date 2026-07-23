"""
Blueprint da agenda médica.

Contém a tela principal (renderiza o HTML com a tabela vazia) e o
endpoint "/api/agendamentos", que o JavaScript do navegador consome
via fetch() para preencher a tabela do Tabulator.

Separar "página" de "dados" (endpoint JSON) facilita tanto os testes
automatizados quanto uma futura busca/filtro sem recarregar a página.
"""

from flask import Blueprint, jsonify, render_template, request, session

from .api_client import ErroAPIAgendamentos, buscar_agendamentos
from .auth import login_required

bp = Blueprint("agenda", __name__)


@bp.route("/")
@login_required
def index():
    return render_template("agenda.html", usuario_nome=session.get("usuario_nome"))


@bp.route("/api/agendamentos")
@login_required
def api_agendamentos():
    """
    Retorna os agendamentos em JSON, já filtrados pelo termo de busca
    (paciente, CPF ou médico), se algum for informado.

    Em caso de falha na API externa, devolve status 502 (Bad Gateway)
    com uma mensagem amigável, em vez de deixar a exceção estourar.
    """
    termo_busca = request.args.get("busca", "").strip().lower()

    try:
        agendamentos = buscar_agendamentos()
    except ErroAPIAgendamentos as erro:
        return jsonify({"erro": str(erro), "agendamentos": []}), 502

    if termo_busca:
        agendamentos = [
            item for item in agendamentos
            if termo_busca in item["paciente"].lower()
            or termo_busca in item["cpf"].lower()
            or termo_busca in item["medico"].lower()
        ]

    return jsonify({"erro": None, "agendamentos": agendamentos})
