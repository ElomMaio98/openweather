import os
import logging
import json
from dotenv import load_dotenv

from pyflink.common import SimpleStringSchema, Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions

# Carrega as variáveis de ambiente e configura o logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Seção de Configurações Lidas do Ambiente ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_RAW_TOPIC")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP")

# CORREÇÃO: Usando os nomes corretos das variáveis de ambiente para o DB
DB_URL = f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def create_flink_environment():
    """Cria e configura o ambiente de execução do Flink."""
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Esta parte de adicionar JARs é para execução local.
    # No Railway, teríamos que construir uma imagem Docker customizada para o Flink.
    # Por enquanto, vamos manter para consistência.
    kafka_jar = f"file://{os.path.abspath('flink_jars/flink-sql-connector-kafka-3.0.1-1.17.jar')}"
    postgres_jar = f"file://{os.path.abspath('flink_jars/postgresql-42.7.1.jar')}"
    env.add_jars(kafka_jar, postgres_jar)
    return env

def process_stream(data_stream):
    """Aplica a lógica de negócio (transformação) no stream de dados."""
    def parse_json(json_str):
        return json.loads(json_str)

    def transform_weather_data(data):
        temp_k = data.get('temperature_kelvin', 0) # Usar .get() para segurança
        temp_c = round(temp_k - 273.15, 2)
        return (
            data.get('city', 'N/A'), temp_c, data.get('humidity', 0), data.get('pressure', 0),
            data.get('wind_speed', 0), data.get('timestamp_unix', 0)
        )

    return data_stream \
        .map(parse_json, output_type=Types.PICKLED_BYTE_ARRAY()) \
        .map(transform_weather_data, output_type=Types.ROW([
            Types.STRING(), Types.FLOAT(), Types.INT(), Types.INT(), Types.FLOAT(), Types.LONG()
        ]))

def main():
    logging.info("Iniciando job Flink...")

    # Bloco de validação para "falhar rápido"
    required_vars = [KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_CONSUMER_GROUP, DB_URL, DB_USER, DB_PASSWORD]
    if not all(required_vars):
        raise ValueError("ERRO FATAL: Uma ou mais variáveis de ambiente para Kafka ou DB não foram configuradas.")

    env = create_flink_environment()

    kafka_consumer = FlinkKafkaConsumer(
        topics=KAFKA_TOPIC,
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': KAFKA_CONSUMER_GROUP + "_flink"
        }
    )
    raw_stream = env.add_source(kafka_consumer)

    processed_stream = process_stream(raw_stream)

    jdbc_sink = JdbcSink.sink(
        "INSERT INTO weather_metrics (city, temperature_celsius, humidity, pressure, wind_speed, timestamp_unix) VALUES (?, ?, ?, ?, ?, ?)",
        JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url(DB_URL) # CORREÇÃO: Usando a variável correta
            .with_driver_name("org.postgresql.Driver")
            .with_user_name(DB_USER) # CORREÇÃO: Usando a variável correta
            .with_password(DB_PASSWORD) # CORREÇÃO: Usando a variável correta
            .build(),
        type_info=Types.ROW([Types.STRING(), Types.FLOAT(), Types.INT(), Types.INT(), Types.FLOAT(), Types.LONG()])
    )
    
    processed_stream.add_sink(jdbc_sink)

    env.execute("Weather Data Processing Job")

if __name__ == "__main__":
    main()