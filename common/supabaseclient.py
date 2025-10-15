import os
from supabase import create_client, Client
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY são obrigatórios!")
        
        self.client: Client = create_client(self.url, self.key)
        logger.info(f"Cliente Supabase conectado: {self.url}")
    
    def insert_data(self, data):
        """Insere dados na tabela weather_metrics"""
        try:
            # Prepara os dados
            record = {
                'city': data.get('city'),
                'temperatura_celsius': data.get('temperature_celsius'),
                'humidity': data.get('humidity'),
                'pressure': data.get('pressure'),
                'wind_speed': data.get('wind_speed'),
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Insere no Supabase
            response = self.client.table('weather_metrics').insert(record).execute()
            
            # Verifica se inseriu com sucesso
            if response.data:
                logger.debug(f"✅ Dados inseridos: {data.get('city')} (ID: {response.data[0].get('id')})")
                return True
            else:
                logger.warning(f"⚠️ Resposta vazia ao inserir: {data.get('city')}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao inserir dados no Supabase: {e}")
            return False
    
    def close(self):
        """Supabase não precisa fechar conexão (HTTP)"""
        logger.info("Cliente Supabase finalizado")