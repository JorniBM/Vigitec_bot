import os
from pyrogram import Client, filters
from dotenv import load_dotenv

from comandos import (
start_command, 
help_command, 
buscar_command, 
favoritos_command, 
configurar_command,
siguiente_command
)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot, API ID y API Hash desde .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Crear una instancia del cliente de Pyrogram usando API ID y API Hash
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Registrar los comandos (importados desde comandos.py)
start_command(app)
help_command(app)
buscar_command(app)
favoritos_command(app) 
configurar_command(app)
siguiente_command(app)


# Definir el manejador de mensajes de texto
@app.on_message(filters.text)
def handle_message(client, message):
    message.reply_text(f"Hola, {message.from_user.first_name}! Has dicho: {message.text}")
    
    

# Iniciar el bot
if __name__ == "__main__":
    print("El bot está corriendo...")
    app.run()
