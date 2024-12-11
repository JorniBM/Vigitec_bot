import unittest
from unittest.mock import MagicMock
from comandos import start_logic, register_start_command

class TestStartCommand(unittest.TestCase):
    def setUp(self):
        # Simulamos un cliente y un mensaje de un usuario
        self.app = MagicMock()
        self.client = MagicMock()
        self.message = MagicMock()
        self.message.from_user.first_name = "Juan"
        
        # Registramos el comando start
        register_start_command(self.app)

    def test_start_message(self):
        # Simulamos el comando /start
        self.app.on_message.return_value = None
        self.app.on_message.call_args[0][1](self.client, self.message)
        
        # Verificamos que el mensaje de bienvenida es el correcto
        self.message.reply_text.assert_called_with("¡Hola, Juan! Bienvenido al chatbot de análisis científico VIGITEC. Usa /help para ver los comandos disponibles.")

if __name__ == '__main__':
    unittest.main()
