# Biblioteca — atividades da 2ª etapa

Aplicação Flask com Jinja2, Bootstrap, formulários e CRUD completo usando
Flask-SQLAlchemy e SQLite.

O mesmo projeto atende às atividades progressivas:

- Atividades em sala — Flask 2;
- Atividade em sala — Jinja2;
- Atividades em Sala — Formulários;
- Atividades em Sala — Formulário Update;
- Atividade SQLAlchemy.

## Funcionalidades

- listagem dos livros em uma tabela;
- cadastro, edição e exclusão;
- validação dos formulários;
- persistência em SQLite com SQLAlchemy;
- API JSON com operações GET, POST, PUT e DELETE;
- template base e estilização com Bootstrap;
- banco criado automaticamente ao iniciar a aplicação.

## Como executar

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Abra `http://127.0.0.1:5000` no navegador.

## Rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Lista os livros |
| GET/POST | `/livros/novo` | Cadastra um livro |
| GET/POST | `/livros/<id>/editar` | Atualiza um livro |
| POST | `/livros/<id>/excluir` | Exclui um livro |
| GET/POST | `/api/livros` | Lista ou cria pela API |
| GET/PUT/DELETE | `/api/livros/<id>` | Consulta, atualiza ou exclui pela API |
