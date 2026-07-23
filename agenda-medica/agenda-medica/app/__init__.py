"""
Application factory da Agenda Médica.

Usamos o padrão "create_app()" (recomendado pela própria documentação
do Flask) em vez de um app global, porque isso facilita muito criar
instâncias separadas para os testes automatizados, cada uma com seu
próprio banco de dados temporário.
"""

import os

from flask import Flask, render_template

# templates/ e static/ ficam na raiz do projeto (fora do pacote "app"),
# então precisamos indicar os caminhos explicitamente.
_DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_TEMPLATES = os.path.join(_DIRETORIO_RAIZ, "templates")
_PASTA_STATIC = os.path.join(_DIRETORIO_RAIZ, "static")


def create_app(config_extra=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=_PASTA_TEMPLATES,
        static_folder=_PASTA_STATIC,
    )
    app.config.from_object("app.config.Config")

    if config_extra:
        app.config.update(config_extra)

    # Garante que a pasta onde o arquivo .sqlite será criado existe.
    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import agenda
    app.register_blueprint(agenda.bp)

    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("erro.html", mensagem="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_interno(erro):
        return render_template("erro.html", mensagem="Erro interno no servidor."), 500

    return app
