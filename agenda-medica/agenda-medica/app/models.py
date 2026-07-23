"""
Funções relacionadas à tabela "usuarios".

Mantemos aqui apenas o acesso a dados (queries SQL) e a lógica de
validação de senha. As rotas (auth.py) chamam essas funções em vez de
montar SQL diretamente, o que separa responsabilidades e facilita
testar cada parte isoladamente.
"""

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


def buscar_usuario_por_login(usuario_ou_email):
    """
    Busca um usuário pelo campo "usuario" OU "email".

    Isso permite que a tela de login aceite tanto o nome de usuário
    quanto o e-mail, como pedido no desafio.
    """
    db = get_db()
    return db.execute(
        "SELECT * FROM usuarios WHERE usuario = ? OR email = ?",
        (usuario_ou_email, usuario_ou_email),
    ).fetchone()


def validar_credenciais(usuario_ou_email, senha):
    """
    Confere usuário e senha.

    Retorna a linha do usuário se as credenciais forem válidas,
    ou None caso contrário (usuário inexistente ou senha incorreta).
    """
    usuario = buscar_usuario_por_login(usuario_ou_email)

    if usuario is None:
        return None

    if not check_password_hash(usuario["senha_hash"], senha):
        return None

    return usuario


def criar_usuario(usuario, email, senha):
    """Cria um novo usuário com a senha já criptografada (hash)."""
    db = get_db()
    senha_hash = generate_password_hash(senha)
    db.execute(
        "INSERT INTO usuarios (usuario, email, senha_hash) VALUES (?, ?, ?)",
        (usuario, email, senha_hash),
    )
    db.commit()
