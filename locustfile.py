from locust import HttpUser, task, between
import random

TELEGRAM_API_URL = "https://api.telegram.org/bot7060266556:AAHO0k7Ynn4O0sxd6kMZlX22Bxz5AE2T9JI/"
CHAT_ID = "863880887"  # Reemplaza con tu chat_id

# Lista de términos de búsqueda para simular la entrada de un término aleatorio
search_terms = ["medicina", "inteligencia artificial", "software"]

class TelegramBotUser(HttpUser):
    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre cada acción

    @task
    def buscar_command(self):
        # Selecciona un término de búsqueda aleatorio de la lista
        search_term = random.choice(search_terms)
        search_text = f"/buscar {search_term}"  # Simula el comando con el término de búsqueda

        # Realiza la solicitud con el término de búsqueda
        response = self.client.get(f"{TELEGRAM_API_URL}sendMessage?chat_id={CHAT_ID}&text={search_text}")
        print(response.text)  # Para ver la respuesta del bot en la terminal
