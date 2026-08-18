import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
ARQUIVO = Path(__file__).with_name("livros.json")


def acessar_livros(acao, isbn=None, dados=None):
    """Concentra leitura e escrita do arquivo em uma unica funcao."""
    if not ARQUIVO.exists():
        ARQUIVO.write_text("[]", encoding="utf-8")
    livros = json.loads(ARQUIVO.read_text(encoding="utf-8"))

    if acao == "listar":
        return livros
    if acao == "buscar":
        return next((livro for livro in livros if livro["isbn"] == isbn), None)
    if acao == "criar":
        if any(livro["isbn"] == dados["isbn"] for livro in livros):
            raise ValueError("ISBN ja cadastrado.")
        livros.append(dados)
    elif acao == "atualizar":
        livro = next((item for item in livros if item["isbn"] == isbn), None)
        if livro is None:
            return None
        livro.update(dados)
    elif acao == "excluir":
        livro = next((item for item in livros if item["isbn"] == isbn), None)
        if livro is None:
            return None
        livros.remove(livro)
    else:
        raise ValueError("Acao invalida.")

    ARQUIVO.write_text(json.dumps(livros, ensure_ascii=False, indent=2), encoding="utf-8")
    return dados if acao != "excluir" else True


@app.route("/livros", methods=["GET", "POST"])
def colecao_livros():
    if request.method == "GET":
        return jsonify(acessar_livros("listar"))
    dados = request.get_json(silent=True) or {}
    campos = ("isbn", "titulo", "autor", "editora", "ano_publicacao")
    if not all(campo in dados for campo in campos):
        return jsonify({"erro": "Informe todos os campos."}), 400
    try:
        return jsonify(acessar_livros("criar", dados=dados)), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@app.route("/livros/<isbn>", methods=["GET", "PUT", "DELETE"])
def item_livro(isbn):
    if request.method == "GET":
        livro = acessar_livros("buscar", isbn=isbn)
        return (jsonify(livro), 200) if livro else (jsonify({"erro": "Nao encontrado."}), 404)
    if request.method == "PUT":
        livro = acessar_livros("atualizar", isbn=isbn, dados=request.get_json() or {})
        return (jsonify(livro), 200) if livro else (jsonify({"erro": "Nao encontrado."}), 404)
    excluido = acessar_livros("excluir", isbn=isbn)
    return ("", 204) if excluido else (jsonify({"erro": "Nao encontrado."}), 404)


if __name__ == "__main__":
    app.run(debug=True)
