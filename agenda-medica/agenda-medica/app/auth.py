"""
Blueprint responsável pela autenticação: tela de login, logout e o
decorator "login_required", usado para proteger as rotas da agenda.
"""

import functools
import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .models import validar_credenciais

bp = Blueprint("auth", __name__)


def login_required(view):
    """
    Decorator que redireciona para a tela de login caso o usuário
    não esteja autenticado (sem "usuario_id" na sessão).
    """

    @functools.wraps(view)
    def view_protegida(*args, **kwargs):
        if session.get("usuario_id") is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return view_protegida


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Se o usuário já está logado
        if session.get("usuario_id") is not None:
            return redirect(url_for("agenda.index"))
        return render_template("login.html")

    usuario_ou_email = request.form.get("usuario", "").strip()
    senha = request.form.get("senha", "")

    # Campos obrigatórios ausentes
    if not usuario_ou_email or not senha:
        flash("Informe usuário/e-mail e senha.", "erro")
        return render_template("login.html"), 400

    try:
        usuario = validar_credenciais(usuario_ou_email, senha)
    except sqlite3.Error:
        # Erro de conexão/consulta ao banco de dados.
        flash("Não foi possível acessar o banco de dados. Tente novamente mais tarde.", "erro")
        return render_template("login.html"), 500

    if usuario is None:
        flash("Usuário ou senha inválidos.", "erro")
        return render_template("login.html"), 401

    session.clear()
    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["usuario"]
    return redirect(url_for("agenda.index"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
