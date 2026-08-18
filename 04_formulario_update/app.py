import json
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "biblioteca-update"
ARQUIVO = Path(__file__).with_name("livros.json")


def carregar_livros():
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def salvar_livros(livros):
    ARQUIVO.write_text(json.dumps(livros, ensure_ascii=False, indent=2), encoding="utf-8")


def dados_formulario():
    return {
        "isbn": request.form["isbn"].strip(),
        "titulo": request.form["titulo"].strip(),
        "autor": request.form["autor"].strip(),
        "editora": request.form["editora"].strip(),
        "ano_publicacao": int(request.form["ano_publicacao"]),
        "quantidade": int(request.form["quantidade"]),
    }


@app.get("/")
def index():
    return render_template("index.html", livros=carregar_livros())


@app.route("/livros/novo", methods=["GET", "POST"])
def criar_livro():
    if request.method == "POST":
        livros = carregar_livros()
        livros.append(dados_formulario())
        salvar_livros(livros)
        flash("Livro cadastrado com sucesso.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", livro=None)


@app.route("/livros/<isbn>/editar", methods=["GET", "POST"])
def editar_livro(isbn):
    livros = carregar_livros()
    livro = next((item for item in livros if item["isbn"] == isbn), None)
    if livro is None:
        flash("Livro nao encontrado.", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        livro.update(dados_formulario())
        salvar_livros(livros)
        flash("Livro atualizado com sucesso.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", livro=livro)


if __name__ == "__main__":
    app.run(debug=True)
