import json
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)
ARQUIVO = Path(__file__).with_name("livros.json")


def carregar_livros():
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


@app.get("/")
def index():
    return render_template("index.html", livros=carregar_livros())


if __name__ == "__main__":
    app.run(debug=True)
