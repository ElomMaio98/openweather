import requests
from requests.exceptions import RequestException

class WeatherAPIClient:
    def __init__(self, WEATHER_KEY, base_url):
        if not WEATHER_KEY:
            raise ValueError("A chave de API é obrigatória. Não estou encontrando.")
        self.WEATHER_KEY = WEATHER_KEY
        self.base_url = base_url
    
    def get_weather(self, lat, lon):
        params = {'lat': lat, 'lon': lon, 'appid': self.WEATHER_KEY, 'units': 'metric'}
        try:
            response =  requests.get(self.base_url, params = params)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return None
        