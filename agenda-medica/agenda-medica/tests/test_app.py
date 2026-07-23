"""
Testes automatizados da Agenda Médica.

Cobrem, no mínimo, os comportamentos sugeridos no desafio:
  - login válido e inválido;
  - retorno sem agendamentos (busca sem correspondência);
  - falha na API de agendamentos.
"""

from unittest.mock import patch

from app.api_client import ErroAPIAgendamentos
from tests.conftest import login

AGENDAMENTO_EXEMPLO = {
    "paciente": "Maria Silva",
    "cpf": "111.111.111-11",
    "medico": "Dr. João Souza",
    "especialidade": "Cardiologia",
    "data": "2026-07-23",
    "horario": "09:00",
    "convenio": "Unimed",
    "status": "Confirmado",
}


def test_login_valido_redireciona_para_agenda(client):
    resposta = login(client)
    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/"


def test_login_invalido_mostra_mensagem_de_erro(client):
    resposta = login(client, senha="senha-errada")
    assert resposta.status_code == 401
    assert "inválidos" in resposta.get_data(as_text=True)


def test_login_com_campos_vazios_e_rejeitado(client):
    resposta = client.post("/login", data={"usuario": "", "senha": ""})
    assert resposta.status_code == 400


def test_pagina_da_agenda_exige_login(client):
    resposta = client.get("/", follow_redirects=False)
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_endpoint_de_agendamentos_exige_login(client):
    resposta = client.get("/api/agendamentos", follow_redirects=False)
    assert resposta.status_code == 302


def test_busca_sem_correspondencia_retorna_lista_vazia(client):
    login(client)

    with patch("app.agenda.buscar_agendamentos") as mock_buscar:
        mock_buscar.return_value = [AGENDAMENTO_EXEMPLO]

        resposta = client.get("/api/agendamentos?busca=paciente-que-nao-existe")

        assert resposta.status_code == 200
        dados = resposta.get_json()
        assert dados["agendamentos"] == []


def test_busca_por_paciente_existente_retorna_resultado(client):
    login(client)

    with patch("app.agenda.buscar_agendamentos") as mock_buscar:
        mock_buscar.return_value = [AGENDAMENTO_EXEMPLO]

        resposta = client.get("/api/agendamentos?busca=Maria")

        dados = resposta.get_json()
        assert len(dados["agendamentos"]) == 1
        assert dados["agendamentos"][0]["paciente"] == "Maria Silva"


def test_falha_na_api_retorna_erro_502(client):
    login(client)

    with patch("app.agenda.buscar_agendamentos") as mock_buscar:
        mock_buscar.side_effect = ErroAPIAgendamentos("API indisponível")

        resposta = client.get("/api/agendamentos")

        assert resposta.status_code == 502
        dados = resposta.get_json()
        assert dados["erro"] == "API indisponível"
        assert dados["agendamentos"] == []
