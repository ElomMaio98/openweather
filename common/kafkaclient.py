from kafka import KafkaProducer, KafkaConsumer
import json
import logging
from kafka.errors import KafkaConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers = bootstrap_servers,
                value_serializer = lambda v: json.dumps(v).encode('utf-8'),
                acks = 'all', 
                retries = 3,
                max_in_flight_requests_per_connection = 1)
            logger.info(f"Produtor Kafka conectado em {bootstrap_servers}.")
        except KafkaConnectionError as e:
            logger.error(f"Erro ao se conectar ao Kafka em {bootstrap_servers}. Erro: {e}")
            raise

    def send_message(self, topic, message):
        try: 
            future = self.producer.send(topic, value = message)
            record_metadata = future.get(timeout=10)
            logger.debug(f"Mensagem enviada para {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except Exception as e:
            logging.critical(f"Erro ao enviar a mensagem: {e}")
            raise
    def close(self):
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Fechou o produtor")

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers, topic, group_id):
        try:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                auto_offset_reset='earliest', # Começa do início se for um novo grupo
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            logging.info(f"Consumidor Kafka conectado em {bootstrap_servers}, escutando o tópico '{topic}'.")
        except KafkaConnectionError as e:
            logging.critical(f"Não foi possível conectar ao Kafka em {bootstrap_servers}. Erro: {e}")
            raise
    
    def get_messages(self):
        try:
            for message in self.consumer:
                yield message.value
        except Exception as e:
            logging.critical(f"Erro ao consumir mensagens: {e}")
            raise

    def close(self):
        if self.consumer:
            self.consumer.close()
            logging.info("Consumidor Kafka fechado.")