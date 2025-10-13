import time
import os 
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.apiclient import client
from common.kafkaclient import kafkaproducerclient
import json

load_dotenv()


API_KEY = os.getenv('WEATHER_KEY')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')  
LOCATIONS_CONFIG_PATH = "config/locations.json"
PRODUCER_SLEEP_SECONDS = int(os.getenv('PRODUCER_SLEEP_SECONDS', 10))
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'dados_brutos')

def locations(path):
    try: 
        with open(path, 'r', encoding='utf-8') as file:
            locations = json.load(file)
            return locations
    except FileNotFoundError:
        print(f"Arquivo de configuração não encontrado: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON: {path}")
        return
    
def main():
    if not all([API_KEY, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC]):
        print("Por favor, defina as variáveis de ambiente WEATHER_KEY e KAFKA_BOOTSTRAP_SERVERS.")
        return
    if not locations:
        print("AVISO: Nenhum local para processar. Verifique o arquivo 'config/locations.json'. Encerrando o programa.")
        return
    weather_client = client.WeatherClient(API_KEY)
    kafka_producer = kafkaproducerclient.KafkaProducerClient(bootstrap = KAFKA_BOOTSTRAP_SERVERS)

    while True:
        for location in locations:
            try: 
                weather_data = weather_client.get_weather(lat=location["lat"], lon=location["lon"])
                message = {
                    "city": weather_data.get('name'),
                    "temperature_kelvin": weather_data['main']['temp'],
                    "humidity": weather_data['main']['humidity'],
                    "pressure": weather_data['main']['pressure'],
                    "wind_speed": weather_data['wind']['speed'],
                    "timestamp_unix": weather_data.get('dt')
                }
                kafka_producer.send_message(KAFKA_TOPIC, message)
            except Exception as e:
                print(f"Erro ao processar a localização {location}: {e}")
if __name__ == "__main__":
    main()