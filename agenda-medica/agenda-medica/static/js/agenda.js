/*
 * Lógica da tela principal da agenda.
 *
 * Busca os agendamentos no endpoint "/api/agendamentos" (backend Flask,
 * que por sua vez chama a API externa) e renderiza os dados na tabela
 * usando a biblioteca Tabulator.
 */

let tabela = null;

function mostrarMensagem(texto, tipo) {
    const elemento = document.getElementById("mensagem-status");
    elemento.textContent = texto;
    elemento.className = "mensagem-status mensagem-" + tipo;
    elemento.style.display = "block";
}

function esconderMensagem() {
    const elemento = document.getElementById("mensagem-status");
    elemento.style.display = "none";
}

function carregarAgendamentos(termoBusca) {
    esconderMensagem();

    let url = "/api/agendamentos";
    if (termoBusca) {
        url += "?busca=" + encodeURIComponent(termoBusca);
    }

    fetch(url)
        .then(function (resposta) {
            return resposta.json().then(function (dados) {
                return { status: resposta.status, dados: dados };
            });
        })
        .then(function (resultado) {
            const dados = resultado.dados;

            if (resultado.status !== 200) {
                // Erro vindo da API externa (indisponibilidade, timeout, etc).
                mostrarMensagem(dados.erro || "Não foi possível carregar os agendamentos.", "erro");
                renderizarTabela([]);
                return;
            }

            if (!dados.agendamentos || dados.agendamentos.length === 0) {
                mostrarMensagem("Nenhum agendamento encontrado.", "aviso");
            }

            renderizarTabela(dados.agendamentos || []);
        })
        .catch(function () {
            // Falha de rede entre o navegador e o próprio backend Flask.
            mostrarMensagem("Erro de comunicação com o servidor. Tente novamente.", "erro");
            renderizarTabela([]);
        });
}

function renderizarTabela(agendamentos) {
    const colunas = [
        { title: "Data", field: "data", width: 110 },
        { title: "Horário", field: "horario", width: 90 },
        { title: "Paciente", field: "paciente" },
        { title: "CPF", field: "cpf", width: 150 },
        { title: "Médico", field: "medico" },
        { title: "Especialidade", field: "especialidade" },
        { title: "Convênio", field: "convenio" },
        { title: "Status", field: "status", width: 120 },
    ];

    if (tabela) {
        tabela.setData(agendamentos);
        return;
    }

    tabela = new Tabulator("#tabela-agendamentos", {
        data: agendamentos,
        columns: colunas,
        layout: "fitColumns",
        placeholder: "Nenhum agendamento disponível",
        pagination: true,
        paginationSize: 10,
    });
}

document.addEventListener("DOMContentLoaded", function () {
    carregarAgendamentos("");

    document.getElementById("botao-buscar").addEventListener("click", function () {
        const termo = document.getElementById("campo-busca").value.trim();
        carregarAgendamentos(termo);
    });

    document.getElementById("campo-busca").addEventListener("keydown", function (evento) {
        if (evento.key === "Enter") {
            carregarAgendamentos(this.value.trim());
        }
    });

    document.getElementById("botao-limpar").addEventListener("click", function () {
        document.getElementById("campo-busca").value = "";
        carregarAgendamentos("");
    });
});
