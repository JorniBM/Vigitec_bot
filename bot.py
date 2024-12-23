import os  # Biblioteca estándar

from dotenv import load_dotenv  # Biblioteca de terceros
from pyrogram import Client, filters  # Biblioteca de terceros

from comandos import (  # Módulos locales
    start_command,
    help_command,
    buscar_command,
    favoritos_command,
    siguiente_command
)


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot, API ID y API Hash desde .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
API_KEY = os.getenv("API_KEY")

# Crear una instancia del cliente de Pyrogram usando API ID y API Hash
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Registrar los comandos (importados desde comandos.py)
start_command(app)
help_command(app)
buscar_command(app)
favoritos_command(app) 
siguiente_command(app)


# Maneja mensajes de texto entrantes y responde con la misma entrada
@app.on_message(filters.text)
def handle_message(client, message):
    message.reply_text(f"Hola, {message.from_user.first_name}! Has dicho: {message.text}")
    
    

# Iniciar el bot
if __name__ == "__main__":
    print("El bot está corriendo...")
    app.run()


