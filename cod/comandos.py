from pyrogram import filters
import requests
import random


# Diccionario global para almacenar los resultados y el índice actual de cada usuario
user_search_results = {}

# Función para enviar mensajes en lotes
def send_separated_messages(client, chat_id, mensajes):
    for mensaje in mensajes:
        client.send_message(chat_id, mensaje)

# Comando /start: Mensaje de bienvenida
def start_command(app):
    @app.on_message(filters.command("start"))
    def start(client, message):
        message.reply_text(f"¡Hola, {message.from_user.first_name}! Bienvenido al chatbot de búsqueda y análisis de información científica en fuentes abiertas Vigitec. Usa /help para ver los comandos disponibles.")

# Comando /help: Muestra los comandos disponibles
def help_command(app): 
    @app.on_message(filters.command("help"))
    def help(client, message):
        comandos = (
            "/buscar [término] - Realiza una búsqueda de artículos científicos en varias bases de datos usando el término indicado, mostrando los resultados más relevantes y recientes.\n"
            "/siguiente - Muestra el siguiente lote de resultados de la búsqueda actual, permitiendo explorar más opciones.\n"
            "/favoritos [numero del articulo] - Añade un artículo a la lista de favoritos.\n"
            "/favoritos - Muestra la lista de artículos favoritos guardados.\n"
            "/favoritos eliminar [numero del articulo] - Elimina un artículo de la lista de favoritos.\n"
            
        )
        message.reply_text(f"Aquí están los comandos disponibles:\n\n{comandos}")

# Funciones de búsqueda
def buscar_semantic_scholar(query):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,authors,year,venue,url,citationCount"
    response = requests.get(url)
    return response.json().get("data", [])

def buscar_crossref(query):
    url = f"https://api.crossref.org/works?query={query}&rows=5&sort=score"
    response = requests.get(url)
    return response.json()["message"]["items"]

def buscar_google_scholar(query):
    api_key = "cb964c23109bfa0f7cb52982e213eb3c29a454212defddc5565ac2c78a744a07"
    url = f"https://serpapi.com/search?engine=google_scholar&q={query}&api_key={api_key}"
    response = requests.get(url)
    return response.json().get("organic_results", [])

# Comando /buscar: Realiza una búsqueda en múltiples APIs con resúmenes completos cuando estén disponibles
def buscar_command(app):
    @app.on_message(filters.command("buscar"))
    def buscar(client, message):
        query = " ".join(message.command[1:])
        if query:
            semantic_scholar_results = buscar_semantic_scholar(query)
            crossref_results = buscar_crossref(query)
            google_scholar_results = buscar_google_scholar(query)

            resultados = []

            # Procesar resultados de Semantic Scholar
            for result in semantic_scholar_results:
                resumen = result.get("abstract", "Resumen no disponible")
                resultados.append({
                    "source": "Semantic Scholar",
                    "title": result.get("title", "Título no disponible"),
                    "authors": ", ".join([author.get("name") for author in result.get("authors", [])]),
                    "year": result.get("year", 0),  # Aseguramos que sea un número
                    "citation_count": result.get("citationCount", 0),
                    "venue": result.get("venue", "No disponible"),
                    "url": result.get("url", "No disponible"),
                    "summary": resumen
                })

            # Procesar resultados de CrossRef
            for item in crossref_results:
                resumen = item.get("abstract", "Resumen no disponible")
                year = item.get("published-print", {}).get("date-parts", [[0]])[0][0] or 0
                resultados.append({
                    "source": "CrossRef",
                    "title": item.get("title", ["No disponible"])[0],
                    "authors": ", ".join([author.get("given", "") + " " + author.get("family", "") for author in item.get("author", [])]),
                    "year": year,
                    "citation_count": item.get("is-referenced-by-count", 0),
                    "venue": item.get("container-title", ["No disponible"])[0],
                    "url": item.get("URL", "No disponible"),
                    "summary": resumen
                })

            # Procesar resultados de Google Scholar
            for item in google_scholar_results:
                resumen = item.get("snippet", "Resumen no disponible")
                resultados.append({
                    "source": "Google Scholar",
                    "title": item.get("title", "No disponible"),
                    "authors": "Autores no disponibles",
                    "year": int(item.get("publication_info", {}).get("year", 0)),  # Convertir el año a int
                    "citation_count": item.get("inline_links", {}).get("cited_by", {}).get("total", 0),
                    "venue": item.get("publication_info", {}).get("venue", "Publicación no disponible"),
                    "url": item.get("link", "No disponible"),
                    "summary": resumen
                })

            # Ordenar por año y luego por cantidad de citas
            resultados = sorted(
                resultados,
                key=lambda x: (int(x["year"]) if isinstance(x["year"], int) else 0, x.get("citation_count", 0)),
                reverse=True
            )

            # Mezclar aleatoriamente los resultados antes de mostrar
            random.shuffle(resultados)

            # Guardar los resultados y el índice de la primera página para este usuario
            user_id = message.from_user.id
            user_search_results[user_id] = {'results': resultados, 'index': 0}

            # Mostrar los primeros 5 resultados
            mostrar_resultados(client, message.chat.id, user_id)
        else:
            message.reply_text("Por favor, introduce un término de búsqueda. Ejemplo: /buscar machine learning")

# Función para mostrar 5 resultados y actualizar el índice para el usuario
def mostrar_resultados(client, chat_id, user_id):
    search_data = user_search_results.get(user_id)
    if not search_data:
        client.send_message(chat_id, "No hay resultados disponibles.")
        return

    results = search_data['results']
    index = search_data['index']
    next_index = index + 5

    # Mostrar hasta 5 resultados con resumen incluido
    message_list = results[index:next_index]
    send_separated_messages(client, chat_id, [
        f"{i+1}. {res['source']}\nTítulo: {res['title']}\nAutores: {res['authors']}\nAño: {res['year']}\nPublicación: {res['venue']}\nEnlace: {res['url']}\nResumen: {res['summary']}\nCitas: {res['citation_count']}\n{'-'*30}"
        for i, res in enumerate(message_list)
    ])

    # Actualizar el índice para el siguiente grupo
    user_search_results[user_id]['index'] = next_index

    # Mostrar opción de "siguiente" si quedan más resultados
    if next_index < len(results):
        client.send_message(chat_id, "Escribe /siguiente para ver más resultados.")

# Comando /siguiente para mostrar más resultados
def siguiente_command(app):
    @app.on_message(filters.command("siguiente"))
    def siguiente(client, message):
        user_id = message.from_user.id
        if user_id in user_search_results:
            mostrar_resultados(client, message.chat.id, user_id)
        else:
            message.reply_text("No hay una búsqueda en curso. Usa /buscar [término] para comenzar una nueva búsqueda.")

# Diccionario global para almacenar los favoritos de cada usuario
user_favorites = {}

# Comando /favoritos: Permite añadir, listar y eliminar artículos favoritos
def favoritos_command(app): 
    @app.on_message(filters.command("favoritos"))
    def favoritos(client, message):
        user_id = message.from_user.id
        command_parts = message.text.split()

        # Verifica si se quiere eliminar un artículo
        if len(command_parts) > 2 and command_parts[1].lower() == "eliminar" and command_parts[2].isdigit():
            article_number = int(command_parts[2]) - 1  # Convertimos a índice (base 0)
            favoritos = user_favorites.get(user_id, [])

            if 0 <= article_number < len(favoritos):
                removed_article = favoritos.pop(article_number)  # Elimina el artículo de favoritos
                message.reply_text(f"Artículo '{removed_article['title']}' eliminado de tus favoritos.")
                
                # Actualiza la lista si queda vacía
                if not favoritos:
                    del user_favorites[user_id]
            else:
                message.reply_text("Número de artículo no válido en la lista de favoritos.")

        # Verifica si hay un número de artículo para agregar
        elif len(command_parts) > 1 and command_parts[1].isdigit():
            article_number = int(command_parts[1]) - 1
            search_data = user_search_results.get(user_id)

            if search_data and 0 <= article_number < len(search_data['results']):
                article = search_data['results'][article_number]

                # Añadir el artículo a favoritos
                if user_id not in user_favorites:
                    user_favorites[user_id] = []
                user_favorites[user_id].append(article)

                message.reply_text(f"Artículo '{article['title']}' añadido a favoritos.")
            else:
                message.reply_text("El número de artículo no es válido o no hay una búsqueda en curso.")

        # Mostrar la lista de favoritos
        else:
            favoritos = user_favorites.get(user_id, [])
            if favoritos:
                favoritos_text = "\n\n".join([
                    f"{i + 1}. {fav['source']}\nTítulo: {fav['title']}\nAutores: {fav['authors']}\nAño: {fav['year']}\nEnlace: {fav['url']}"
                    for i, fav in enumerate(favoritos)
                ])
                message.reply_text(f"Tus artículos favoritos:\n\n{favoritos_text}\n")
            else:
                message.reply_text("No tienes artículos guardados en favoritos.")






  
        


