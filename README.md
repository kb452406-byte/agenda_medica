Agenda Médica
Aplicação web simples de agenda médica, feita em Python com Flask. Permite login de usuário, consulta de agendamentos vindos de uma API (simulada como um serviço HTTP separado) e busca por paciente, CPF ou médico, exibindo os dados em uma tabela interativa (Tabulator).

Estrutura do projeto
agenda-medica/
├── app/                    # Código da aplicação principal (Flask)
│   ├── __init__.py         # Application factory (create_app)
│   ├── config.py           # Configurações (lidas de variáveis de ambiente)
│   ├── db.py                # Conexão e inicialização do SQLite
│   ├── schema.sql          # Criação da tabela de usuários
│   ├── models.py           # Queries SQL relacionadas a usuários
│   ├── seed.py              # Cria o usuário de teste
│   ├── auth.py              # Rotas de login/logout + login_required
│   ├── agenda.py            # Tela principal + endpoint /api/agendamentos
│   └── api_client.py        # Integração HTTP com a API de agendamentos
├── templates/                # HTML (login, agenda, página de erro)
├── static/                   # CSS e JavaScript (Tabulator + fetch)
├── mock_api/                 # API simulada de agendamentos (serviço separado)
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── tests/                    # Testes automatizados (pytest)
├── run.py                    # Ponto de entrada da aplicação
├── requirements.txt
├── requirements-dev.txt      # Dependências extras para rodar os testes
├── Dockerfile
├── docker-compose.yml
└── .env.example
Como rodar com Docker (recomendado)
Basta um único comando para subir a aplicação e a API simulada:

docker-compose up --build
Aplicação principal: http://localhost:5000
API simulada de agendamentos: http://localhost:5001/agendamentos
O banco de dados é criado automaticamente na primeira execução, junto com o usuário de teste (usuário: medico, senha: 123456).

Como rodar localmente (sem Docker)
Em dois terminais separados:

# Terminal 1: API simulada de agendamentos
cd mock_api
pip install -r requirements.txt
python app.py

# Terminal 2: aplicação principal
cd agenda-medica
pip install -r requirements.txt
export API_URL=http://localhost:5001/agendamentos   # no Windows: set API_URL=...
python run.py
Acesse http://localhost:5000 e faça login com medico / 123456.

Como rodar os testes
pip install -r requirements-dev.txt
pytest
Os testes usam um banco SQLite temporário (criado e apagado a cada execução) e simulam ("mockam") a chamada à API de agendamentos, então não é necessário ter o mock_api rodando para testar.

Decisões de projeto
SQLite acessado diretamente via sqlite3, sem ORM: o objetivo é deixar as queries SQL explícitas e fáceis de ler, já que um dos pontos avaliados é o conhecimento de banco de dados SQL.
API de agendamentos como serviço HTTP separado (mock_api/): representa de forma realista uma integração externa, permitindo testar cenários como indisponibilidade (SIMULAR_FALHA=1) sem alterar o código da aplicação principal.
Toda a lógica de chamada HTTP concentrada em api_client.py: as rotas nunca lidam diretamente com requests ou exceções de rede; elas apenas tratam a exceção ErroAPIAgendamentos, com mensagem já pronta para o usuário.
Sessão simples do Flask para login, sem bibliotecas externas de autenticação, para manter o fluxo fácil de acompanhar.
Cenários de erro tratados
Cenário	Como é tratado
Credenciais de login inválidas	Mensagem "Usuário ou senha inválidos" na tela de login (HTTP 401)
Nenhum agendamento encontrado	Mensagem "Nenhum agendamento encontrado" na tela, tabela vazia
Resposta vazia ou inválida da API	Tratada como lista vazia ou erro amigável, sem quebrar a aplicação
Indisponibilidade temporária da API	Mensagem "Não foi possível conectar à API de agendamentos" (HTTP 502)
Erro de conexão com o banco de dados	Mensagem "Não foi possível acessar o banco de dados" no login
Campos obrigatórios ausentes na resposta	Registros incompletos são descartados silenciosamente da listagem
Testando a indisponibilidade da API manualmente
Com o docker-compose rodando, edite a variável SIMULAR_FALHA do serviço mock_api no docker-compose.yml para 1 e reinicie:

docker-compose up --build mock_api
A tela da agenda deve exibir a mensagem de erro amigável em vez de quebrar a página.
