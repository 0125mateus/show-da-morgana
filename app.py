"""
Sistema de confirmação de presença — O Show da Morgana.

Rodar:
    pip install -r requirements.txt
    python app.py

Letreiro:  http://127.0.0.1:5000/
Formulário: http://127.0.0.1:5000/confirmar
Painel:     http://127.0.0.1:5000/admin
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

from models import EVENTO, formatar_data_br, prazo_aberto
from storage import adicionar, excluir, listar, resumo

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "show-da-morgana-2026")

COMPONENTS_DIR = Path(__file__).resolve().parent / "components"
THEATER_CURTAIN_DIR = COMPONENTS_DIR / "theater-curtain"
SHOW_SIGN_DIR = COMPONENTS_DIR / "show-sign"


@app.get("/components/theater-curtain/<path:filename>")
def theater_curtain_asset(filename: str):
    """Serve CSS/JS do componente de cortina (isolado)."""
    return send_from_directory(THEATER_CURTAIN_DIR, filename)


@app.get("/components/show-sign/<path:filename>")
def show_sign_asset(filename: str):
    """Serve CSS/JS do letreiro luminoso."""
    return send_from_directory(SHOW_SIGN_DIR, filename)


def link_whatsapp(texto: str) -> str:
    return f"https://wa.me/{EVENTO.whatsapp}?text={quote(texto)}"


@app.context_processor
def injeta_evento():
    return {
        "evento": EVENTO,
        "data_festa_br": formatar_data_br(EVENTO.data_festa),
        "prazo_br": formatar_data_br(EVENTO.prazo_confirmacao),
        "prazo_ok": prazo_aberto(),
    }


@app.get("/")
def index():
    """Página do vídeo."""
    return render_template("index.html")


@app.route("/confirmar", methods=["GET", "POST"])
def pagina_confirmar():
    """Página do convite + formulário de confirmação."""
    if request.method == "GET":
        return render_template("confirmar.html")

    if not prazo_aberto():
        flash("O prazo de confirmação já encerrou (até 9 de setembro).", "erro")
        return redirect(url_for("pagina_confirmar"))

    nome = (request.form.get("nome") or "").strip()
    status = request.form.get("status", "sim")
    mensagem = (request.form.get("mensagem") or "").strip()

    try:
        adultos = int(request.form.get("adultos") or 0)
        criancas = int(request.form.get("criancas") or 0)
    except ValueError:
        flash("Quantidade de pessoas inválida.", "erro")
        return redirect(url_for("pagina_confirmar"))

    if len(nome) < 2:
        flash("Conta pra gente o seu nome 🙂", "erro")
        return redirect(url_for("pagina_confirmar"))

    if status == "sim" and (adultos + criancas) < 1:
        flash("Informe quantas pessoas vão à festa.", "erro")
        return redirect(url_for("pagina_confirmar"))

    if status == "nao":
        adultos, criancas = 0, 0

    confirmacao = adicionar(nome, adultos, criancas, status, mensagem)

    if confirmacao.status == "sim":
        texto_wa = (
            f"Olá! Confirmo presença no Show da Morgana 🧪\n"
            f"Nome: {confirmacao.nome}\n"
            f"Adultos: {confirmacao.adultos} | Crianças: {confirmacao.criancas}\n"
            f"Total: {confirmacao.total_pessoas} pessoa(s)"
        )
        if confirmacao.mensagem:
            texto_wa += f"\nRecado: {confirmacao.mensagem}"
    else:
        texto_wa = (
            f"Olá! Infelizmente não poderei ir ao Show da Morgana.\n"
            f"Nome: {confirmacao.nome}"
        )

    return render_template(
        "obrigado.html",
        confirmacao=confirmacao,
        whatsapp_url=link_whatsapp(texto_wa),
    )


@app.get("/admin/login")
def admin_login_redirect():
    return redirect(url_for("admin"))


@app.get("/admin")
def admin():
    confirmacoes = listar()
    confirmacoes = sorted(confirmacoes, key=lambda c: c.criado_em, reverse=True)
    return render_template(
        "admin.html",
        confirmacoes=confirmacoes,
        stats=resumo(),
    )


@app.post("/admin/excluir/<confirmacao_id>")
def admin_excluir(confirmacao_id: str):
    if excluir(confirmacao_id):
        flash("Confirmação excluída.", "ok")
    else:
        flash("Confirmação não encontrada.", "erro")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
