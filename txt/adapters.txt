

from abc import ABC, abstractmethod
import requests

# Interfaz común para adaptadores de búsqueda
class ISearchAdapter(ABC):
    @abstractmethod
    def search(self, query):
        pass

class SemanticScholarAdapter(ISearchAdapter):  
    def search(self, query):
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,authors,year,venue,url,citationCount"
        response = requests.get(url)
        return response.json().get("data", [])

class CrossRefAdapter(ISearchAdapter):  
    def search(self, query):
        url = f"https://api.crossref.org/works?query={query}&rows=5&sort=score"
        response = requests.get(url)
        return response.json()["message"]["items"]

class GoogleScholarAdapter(ISearchAdapter):  
    def search(self, query):
        api_key = "TU_API_KEY"
        url = f"https://serpapi.com/search?engine=google_scholar&q={query}&api_key={api_key}"
        response = requests.get(url)
        return response.json().get("organic_results", [])
