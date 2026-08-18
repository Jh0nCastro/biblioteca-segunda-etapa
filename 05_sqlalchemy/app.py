from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "biblioteca-segunda-etapa"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{BASE_DIR / 'biblioteca.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.ensure_ascii = False

db = SQLAlchemy(app)


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "editora": self.editora,
            "ano_publicacao": self.ano_publicacao,
            "quantidade": self.quantidade,
        }


def dados_do_formulario():
    campos = {
        "isbn": request.form.get("isbn", "").strip(),
        "titulo": request.form.get("titulo", "").strip(),
        "autor": request.form.get("autor", "").strip(),
        "editora": request.form.get("editora", "").strip(),
    }

    if not all(campos.values()):
        raise ValueError("Preencha todos os campos obrigatorios.")

    try:
        campos["ano_publicacao"] = int(request.form.get("ano_publicacao", ""))
        campos["quantidade"] = int(request.form.get("quantidade", ""))
    except ValueError as erro:
        raise ValueError("Ano e quantidade devem ser numeros inteiros.") from erro

    if campos["ano_publicacao"] < 0 or campos["quantidade"] < 0:
        raise ValueError("Ano e quantidade nao podem ser negativos.")

    return campos


@app.get("/")
def index():
    livros = db.session.execute(db.select(Livro).order_by(Livro.titulo)).scalars()
    return render_template("index.html", livros=livros)


@app.route("/livros/novo", methods=["GET", "POST"])
def criar_livro():
    if request.method == "POST":
        try:
            livro = Livro(**dados_do_formulario())
            db.session.add(livro)
            db.session.commit()
            flash("Livro cadastrado com sucesso.", "success")
            return redirect(url_for("index"))
        except ValueError as erro:
            flash(str(erro), "danger")
        except Exception:
            db.session.rollback()
            flash("Nao foi possivel cadastrar. Verifique se o ISBN ja existe.", "danger")

    return render_template("form.html", livro=None)


@app.route("/livros/<int:livro_id>/editar", methods=["GET", "POST"])
def editar_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)

    if request.method == "POST":
        try:
            for campo, valor in dados_do_formulario().items():
                setattr(livro, campo, valor)
            db.session.commit()
            flash("Livro atualizado com sucesso.", "success")
            return redirect(url_for("index"))
        except ValueError as erro:
            flash(str(erro), "danger")
        except Exception:
            db.session.rollback()
            flash("Nao foi possivel atualizar. Verifique o ISBN.", "danger")

    return render_template("form.html", livro=livro)


@app.post("/livros/<int:livro_id>/excluir")
def excluir_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    db.session.delete(livro)
    db.session.commit()
    flash("Livro excluido com sucesso.", "success")
    return redirect(url_for("index"))


@app.get("/api/livros")
def api_listar_livros():
    livros = db.session.execute(db.select(Livro).order_by(Livro.titulo)).scalars()
    return jsonify([livro.to_dict() for livro in livros])


@app.get("/api/livros/<int:livro_id>")
def api_obter_livro(livro_id):
    return jsonify(db.get_or_404(Livro, livro_id).to_dict())


@app.post("/api/livros")
def api_criar_livro():
    dados = request.get_json(silent=True) or {}
    campos = ("isbn", "titulo", "autor", "editora", "ano_publicacao", "quantidade")
    if not all(campo in dados for campo in campos):
        return jsonify({"erro": "Informe todos os campos."}), 400

    try:
        livro = Livro(**{campo: dados[campo] for campo in campos})
        db.session.add(livro)
        db.session.commit()
        return jsonify(livro.to_dict()), 201
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Nao foi possivel cadastrar o livro."}), 400


@app.put("/api/livros/<int:livro_id>")
def api_atualizar_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    dados = request.get_json(silent=True) or {}
    campos = ("isbn", "titulo", "autor", "editora", "ano_publicacao", "quantidade")

    for campo in campos:
        if campo in dados:
            setattr(livro, campo, dados[campo])

    try:
        db.session.commit()
        return jsonify(livro.to_dict())
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Nao foi possivel atualizar o livro."}), 400


@app.delete("/api/livros/<int:livro_id>")
def api_excluir_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    db.session.delete(livro)
    db.session.commit()
    return "", 204


def criar_banco():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
