import unittest
from unittest.mock import patch, MagicMock
from comandos import register_buscar_command, buscar_logic  # Asegúrate de importar correctamente tu archivo

class TestBuscarCommandIntegration(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial de la prueba.
        Se crea un cliente simulado y un mensaje de prueba.
        """
        self.client = MagicMock()  # Crear un cliente simulado
        self.message = MagicMock()  # Crear un mensaje simulado
        self.message.from_user.id = 1234  # ID de usuario simulado
        self.message.chat.id = 5678  # ID del chat simulado
        self.message.command = ['/buscar', 'machine learning']  # Simulamos el comando /buscar con un término de búsqueda

        # Registramos el comando /buscar
        self.app = MagicMock()  # Crear una aplicación simulada
        register_buscar_command(self.app)  # Registrar el comando

    @patch('your_bot_file.buscar_crossref')  # Mock de la función buscar_crossref
    @patch('your_bot_file.buscar_semantic_scholar')  # Mock de la función buscar_semantic_scholar
    @patch('your_bot_file.buscar_google_scholar')  # Mock de la función buscar_google_scholar
    def test_buscar_command(self, mock_google_scholar, mock_semantic_scholar, mock_crossref):
        """
        Prueba de integración para el comando /buscar.
        Verifica que al recibir el comando /buscar, se interactúe correctamente con las APIs simuladas.
        """
        # Simular las respuestas de las APIs
        mock_crossref.return_value = [
            {
                'title': 'Machine Learning in Healthcare',
                'author': [{'given': 'John', 'family': 'Doe'}],
                'abstract': 'This paper discusses machine learning...',
                'published-print': {'date-parts': [[2020]]},
                'is-referenced-by-count': 50,
                'container-title': ['Journal of AI'],
                'URL': 'https://doi.org/10.1000/journalai123',
            }
        ]
        mock_semantic_scholar.return_value = []
        mock_google_scholar.return_value = []

        # Llamar al comando /buscar con el término 'machine learning'
        register_buscar_command(self.app)  # Registra el comando
        self.app.on_message.call_args[0][1](self.client, self.message)  # Llamamos al handler del comando /buscar

        # Verificar que las APIs fueron llamadas
        mock_crossref.assert_called_once_with('machine learning')  # Verificar que buscar_crossref fue llamado con el término adecuado
        mock_semantic_scholar.assert_called_once_with('machine learning')
        mock_google_scholar.assert_called_once_with('machine learning')

        # Verificar que el bot responde con el mensaje esperado (los resultados de la búsqueda)
        self.client.send_message.assert_called_once_with(
            self.message.chat.id,
            '1. CrossRef\nTítulo: Machine Learning in Healthcare\nAutores: John Doe\nAño: 2020\nPublicación: Journal of AI\nEnlace: https://doi.org/10.1000/journalai123\nResumen: This paper discusses machine learning...\nCitas: 50\n------------------------------'
        )

if __name__ == '__main__':
    unittest.main()
