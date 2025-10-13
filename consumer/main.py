import json
import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../common')))

from common.databaseclient import postgresclient
from common.kafkaclient import kafkaconsumerclient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    try:
        kafka_client = kafkaconsumerclient(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            topic=os.getenv('KAFKA_TOPIC'),
            group_id=os.getenv('KAFKA_GROUP_ID')
        )
        for message in kafka_client.get_messages():
            logging.debug(f"Mensagem recebida: {message}")
    except Exception as e:
        logging.critical(f"Falha ao inicializar o consumidor Kafka: {e}")
        return
    finally:
        if 'kafka_client' in locals():
            kafka_client.close()

