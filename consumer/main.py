import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.supabaseclient import SupabaseClient  # ✅ NOVO!
from common.kafkaclient import KafkaClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)  

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'dados_brutos')
KAFKA_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP', 'weather-consumer-group')


def validate_environment():
    required_kafka = [KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC]
    required_supabase = [os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')]
    
    if not all(required_kafka):
        logger.error("❌ Variáveis do Kafka faltando")
        return False
    
    if not all(required_supabase):
        logger.error("❌ Variáveis do Supabase faltando")
        return False
    
    return True


def main():
    logger.info("🚀 Iniciando Weather Consumer...")
    
    if not validate_environment():
        logger.error("❌ Encerrando devido a configurações faltantes")
        return
    
    try:
        # Cria AMBOS os clientes
        kafka_client = KafkaClient()
        consumer = kafka_client.create_consumer(
            topic=KAFKA_TOPIC,
            group_id=KAFKA_GROUP_ID
        )
        
        db_client = SupabaseClient()  # ✅ NOVO!
        
        logger.info("✅ Consumer e Supabase conectados com sucesso")
        logger.info(f"📡 Aguardando mensagens do tópico '{KAFKA_TOPIC}'...")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar clientes: {e}")
        return
    
    try:
        message_count = 0
        
        for message in consumer:
            message_count += 1
            data = message.value
            
            try:
                logger.info(f"📩 Mensagem #{message_count}: {data['city']} - {data['temperature_celsius']}°C")
                
                db_client.insert_data(data)
                logger.info(f"✅ Dados salvos no Supabase: {data['city']}")
                
            except KeyError as e:
                logger.error(f"Estrutura de mensagem inválida: {e}")
            except Exception as e:
                logger.error(f"Erro ao processar mensagem: {e}")
                
    except KeyboardInterrupt:
        logger.info("\n⏹️ Consumer interrompido pelo usuário (Ctrl+C)")
    except Exception as e:
        logger.error(f"Erro fatal no consumer: {e}")
    finally:
        kafka_client.close()
        db_client.close()
        logger.info("Consumer finalizado")


if __name__ == "__main__":
    main()
    