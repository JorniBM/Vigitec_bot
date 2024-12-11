import unittest
from comandos import help_logic

class TestHelpLogic(unittest.TestCase):
    def test_help_logic(self):
        expected_response = (
             "/buscar [término] - Realiza una búsqueda de artículos científicos en varias bases de datos usando el término indicado, mostrando los resultados más relevantes y recientes.\n"
            "/siguiente - Muestra el siguiente lote de resultados de la búsqueda actual, permitiendo explorar más opciones.\n"
            "/favoritos [numero del articulo] - Añade un artículo a la lista de favoritos.\n"
            "/favoritos - Muestra la lista de artículos favoritos guardados.\n"
            "/favoritos eliminar [numero del articulo] - Elimina un artículo de la lista de favoritos.\n"
        )
        self.assertEqual(help_logic(), expected_response)
