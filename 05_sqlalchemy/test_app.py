import unittest

from app import Livro, app, db


class BibliotecaTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        )
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crud_web(self):
        resposta = self.client.post(
            "/livros/novo",
            data={
                "isbn": "9788535902778",
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "editora": "Companhia das Letras",
                "ano_publicacao": "1899",
                "quantidade": "3",
            },
            follow_redirects=True,
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Dom Casmurro", resposta.data)

        with app.app_context():
            livro_id = db.session.execute(db.select(Livro.id)).scalar_one()

        resposta = self.client.post(
            f"/livros/{livro_id}/editar",
            data={
                "isbn": "9788535902778",
                "titulo": "Dom Casmurro - Edicao especial",
                "autor": "Machado de Assis",
                "editora": "Companhia das Letras",
                "ano_publicacao": "1899",
                "quantidade": "5",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Edicao especial", resposta.data)

        resposta = self.client.post(
            f"/livros/{livro_id}/excluir", follow_redirects=True
        )
        self.assertNotIn(b"Edicao especial", resposta.data)

    def test_crud_api(self):
        resposta = self.client.post(
            "/api/livros",
            json={
                "isbn": "9786555522266",
                "titulo": "Quarto de Despejo",
                "autor": "Carolina Maria de Jesus",
                "editora": "Atica",
                "ano_publicacao": 1960,
                "quantidade": 2,
            },
        )
        self.assertEqual(resposta.status_code, 201)
        livro_id = resposta.get_json()["id"]

        resposta = self.client.put(
            f"/api/livros/{livro_id}", json={"quantidade": 4}
        )
        self.assertEqual(resposta.get_json()["quantidade"], 4)

        resposta = self.client.delete(f"/api/livros/{livro_id}")
        self.assertEqual(resposta.status_code, 204)


if __name__ == "__main__":
    unittest.main()
