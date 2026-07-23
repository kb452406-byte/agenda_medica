"""
Ponto de entrada da aplicação.

Ao iniciar, garante que o banco de dados existe (init_db) e que o
usuário de teste está cadastrado (seed_test_user). Isso permite que
"docker-compose up" (ou "python run.py") deixe a aplicação pronta
para uso com um único comando, sem passos manuais extras.
"""

from app import create_app
from app import db as db_module
from app import seed

app = create_app()

with app.app_context():
    db_module.init_db()
    seed.seed_test_user()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
