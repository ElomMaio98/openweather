import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.databaseclient import PostgresClient  # ✅
from common.kafkaclient import KafkaConsumerClient  # ✅

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)  # ✅

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP')

DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}


def validate_environment():
    required_kafka = [KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID]
    required_db = list(DB_CONFIG.values())
    
    if not all(required_kafka):
        logger.error("❌ Variáveis do Kafka faltando")
        return False
    
    if not all(required_db):
        logger.error("❌ Variáveis do Postgres faltando")
        return False
    
    return True


def main():
    logger.info("🚀 Iniciando Weather Consumer...")
    
    if not validate_environment():
        logger.error("❌ Encerrando devido a configurações faltantes")
        return
    
    try:
        # Cria AMBOS os clientes
        kafka_consumer = KafkaConsumerClient(  # ✅
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            topic=KAFKA_TOPIC,
            group_id=KAFKA_GROUP_ID
        )
        
        db_client = PostgresClient(DB_CONFIG)  # ✅
        
        logger.info("✅ Consumer e Database conectados com sucesso")
        logger.info(f"📥 Aguardando mensagens do tópico '{KAFKA_TOPIC}'...")
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar clientes: {e}")
        return
    
    try:
        message_count = 0
        
        for message in kafka_consumer.get_messages():
            message_count += 1
            
            try:
                logger.info(f"📨 Mensagem #{message_count}: {message['city']} - {message['temperature_celsius']}°C")
                
                # Salva no banco! ✅
                db_client.insert_data(message)
                
                logger.info(f"✅ Dados salvos no banco: {message['city']}")
                
            except KeyError as e:
                logger.error(f"❌ Estrutura de mensagem inválida: {e}")
            except Exception as e:
                logger.error(f"❌ Erro ao processar mensagem: {e}")
                
    except KeyboardInterrupt:
        logger.info("\nConsumer interrompido pelo usuário (Ctrl+C)")
    except Exception as e:
        logger.error(f"Erro fatal no consumer: {e}")
    finally:
        # Fecha AMBOS os clientes ✅
        kafka_consumer.close()
        db_client.close_pool()
        logger.info("👋 Consumer finalizado")


if __name__ == "__main__":
    main()