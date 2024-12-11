import unittest
from comandos import favoritos_logic

class TestFavoritosLogic(unittest.TestCase):
    def setUp(self):
        # Datos de ejemplo para simular la búsqueda de un usuario
        self.user_id = 12345
        self.user_search_results = {
            self.user_id: {
                'results': [
                    {'title': 'Artículo 1', 'source': 'Fuente A', 'authors': 'Autor A', 'year': 2023, 'url': 'http://url1.com'},
                    {'title': 'Artículo 2', 'source': 'Fuente B', 'authors': 'Autor B', 'year': 2022, 'url': 'http://url2.com'}
                ]
            }
        }
        self.user_favorites = {}

    def test_add_to_favorites(self):
        # Simulamos que el usuario añade el artículo 1 a favoritos
        message_text = "/favoritos 1"
        response = favoritos_logic(self.user_id, message_text)
        self.assertIn("Artículo 'Artículo 1' añadido a favoritos.", response)

    def test_list_favorites(self):
        # Simulamos que el usuario ya tiene artículos en favoritos
        self.user_favorites[self.user_id] = [
            {'title': 'Artículo 1', 'source': 'Fuente A', 'authors': 'Autor A', 'year': 2023, 'url': 'http://url1.com'}
        ]
        
        message_text = "/favoritos"
        response = favoritos_logic(self.user_id, message_text)
        self.assertIn("Tus artículos favoritos:", response)
        self.assertIn("Artículo 1", response)

    def test_no_favorites(self):
        # Verificamos que si no hay favoritos, se devuelve el mensaje adecuado
        message_text = "/favoritos"
        response = favoritos_logic(self.user_id, message_text)
        self.assertEqual(response, "No tienes artículos guardados en favoritos.")

if __name__ == '__main__':
    unittest.main()
