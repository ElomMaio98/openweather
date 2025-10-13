from kafka import KafkaProducer, KafkaConsumer
import json
import logging
from kafka.errors import KafkaConnectionError

class kafkaproducerclient:
    def __init__(self, bootstrapservers):
        self.producer = KafkaProducer(bootstrapservers = bootstrapservers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    def send_message(self, topic, message):
        try: 
            self.producer.send(topic, value = message)
            self.producer.flush()
        except Exception as e:
            logging.critical(f"Erro ao enviar a mensagem: {e}")

class kafkaconsumerclient:
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