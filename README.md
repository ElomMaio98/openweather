# 🌦️ Weather Data Pipeline - Real-Time Streaming

Pipeline de dados em tempo real para coleta, processamento e visualização de dados meteorológicos das principais capitais brasileiras.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Kafka](https://img.shields.io/badge/Kafka-Confluent-black.svg)](https://www.confluent.io/)
[![TimescaleDB](https://img.shields.io/badge/Database-TimescaleDB-orange.svg)](https://www.timescale.com/)
[![Grafana](https://img.shields.io/badge/Visualization-Grafana-orange.svg)](https://grafana.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app/)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Deploy](#deploy)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dashboards](#dashboards)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## 🎯 Sobre o Projeto

Este projeto implementa um **pipeline de dados em tempo real** para:

- 📡 Coletar dados meteorológicos de 27 capitais brasileiras via OpenWeatherMap API
- 📨 Processar dados através de message broker (Apache Kafka)
- 💾 Armazenar em banco de dados otimizado para séries temporais (TimescaleDB)
- 📊 Visualizar em dashboards interativos (Grafana)

### ✨ Funcionalidades

- ✅ Coleta automatizada a cada 5-10 minutos
- ✅ Processamento assíncrono com Kafka
- ✅ Armazenamento eficiente de time-series
- ✅ Dashboards em tempo real
- ✅ Filtros por cidade
- ✅ Visualização geográfica (mapas)
- ✅ Cálculo de médias e estatísticas
- ✅ Deploy cloud-native

---

## 🏗️ Arquitetura

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│              │      │              │      │              │      │              │
│ OpenWeather  │─────▶│   Producer   │─────▶│    Kafka     │─────▶│   Consumer   │
│     API      │      │   (Python)   │      │  (Confluent) │      │   (Python)   │
│              │      │              │      │              │      │              │
└──────────────┘      └──────────────┘      └──────────────┘      └──────┬───────┘
                                                                          │
                                                                          ▼
                      ┌──────────────┐                           ┌──────────────┐
                      │              │                           │              │
                      │   Grafana    │◀──────────────────────────│  TimescaleDB │
                      │  Dashboards  │                           │  (Supabase)  │
                      │              │                           │              │
                      └──────────────┘                           └──────────────┘
```

### Fluxo de Dados

1. **Producer** busca dados da API OpenWeatherMap (temperatura, umidade, pressão, vento)
2. **Kafka** recebe e armazena mensagens no tópico `dados_brutos`
3. **Consumer** processa mensagens e persiste no banco
4. **TimescaleDB** armazena dados otimizados para queries temporais
5. **Grafana** visualiza dados em tempo real

---

## 🛠️ Tecnologias

### Backend & Processing
- **Python 3.11** - Linguagem principal
- **Apache Kafka** - Message broker (Confluent Cloud)
- **kafka-python** - Client Kafka

### Database
- **Supabase** - PostgreSQL gerenciado
- **TimescaleDB** - Extensão para time-series
- **PostGIS** - Dados geoespaciais

### Visualization
- **Grafana** - Dashboards e gráficos

### Infrastructure
- **Railway** - Deploy e hospedagem
- **Docker** - Containerização
- **Git** - Controle de versão

### APIs Externas
- **OpenWeatherMap API** - Dados meteorológicos

---

## ⚙️ Pré-requisitos

### Contas e Credenciais

1. **OpenWeatherMap API**
   - Criar conta em [openweathermap.org](https://openweathermap.org/)
   - Gerar API Key gratuita

2. **Confluent Cloud** (Kafka)
   - Criar conta em [confluent.cloud](https://confluent.cloud/)
   - Criar cluster Kafka
   - Criar API Key e Secret

3. **Supabase**
   - Criar projeto em [supabase.com](https://supabase.com/)
   - Obter URL e API Key

4. **Railway** (para deploy)
   - Criar conta em [railway.app](https://railway.app/)
   - Conectar com GitHub

### Desenvolvimento Local

- Python 3.11+
- pip ou poetry
- Git
- Docker (opcional)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Crie ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

Crie arquivo `.env` na raiz:

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais (veja seção [Configuração](#configuração))

---

## 🔧 Configuração

### Variáveis de Ambiente

#### **OpenWeatherMap API**
```bash
WEATHER_KEY=sua_api_key_aqui
```

#### **Kafka (Confluent Cloud)**
```bash
KAFKA_BOOTSTRAP_SERVERS=pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
KAFKA_SASL_USERNAME=seu_username
KAFKA_SASL_PASSWORD=seu_password
KAFKA_TOPIC=dados_brutos
KAFKA_CONSUMER_GROUP=weather-consumer-group
```

#### **Supabase**
```bash
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_service_role_key
```

#### **Configurações do Producer**
```bash
PRODUCER_SLEEP_SECONDS=300  # 5 minutos (padrão)
```

### Configurar Banco de Dados

Execute no SQL Editor do Supabase:

```sql
-- Criar tabela
CREATE TABLE weather_metrics (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude FLOAT8,
    longitude FLOAT8,
    temperatura_celsius FLOAT4,
    humidity FLOAT4,
    pressure FLOAT4,
    wind_speed FLOAT4,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Criar índices
CREATE INDEX idx_weather_time ON weather_metrics(created_at DESC);
CREATE INDEX idx_weather_city ON weather_metrics(city);

-- Habilitar TimescaleDB (opcional, mas recomendado)
CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT create_hypertable('weather_metrics', 'created_at', 
    chunk_time_interval => INTERVAL '7 days');
```

### Configurar Localizações

Edite `config/locations.json`:

```json
[
  {
    "name": "São Paulo",
    "lat": -23.5505,
    "lon": -46.6333
  },
  {
    "name": "Rio de Janeiro",
    "lat": -22.9068,
    "lon": -43.1729
  }
]
```

---

## 🚀 Como Executar

### Modo Desenvolvimento (Local)

#### 1. Executar Producer

```bash
python producer/main.py
```

Logs esperados:
```
INFO - Iniciando Weather Data Producer
INFO - Intervalo de coleta: 300 segundos
INFO - 27 localizações carregadas
✅ São Paulo: 25.3°C (lat: -23.5505, lon: -46.6333)
```

#### 2. Executar Consumer

Em outro terminal:

```bash
python consumer/main.py
```

Logs esperados:
```
INFO - 🚀 Iniciando Weather Consumer...
INFO - ✅ Consumer e Supabase conectados
INFO - 📡 Aguardando mensagens do tópico 'dados_brutos'...
INFO - 📩 Mensagem #1: São Paulo - 25.3°C
INFO - ✅ Dados salvos no Supabase
```

### Modo Produção (Docker)

#### Producer
```bash
docker build -t weather-producer ./producer
docker run --env-file .env weather-producer
```

#### Consumer
```bash
docker build -t weather-consumer ./consumer
docker run --env-file .env weather-consumer
```

---

## ☁️ Deploy

### Railway

#### 1. Criar projeto no Railway

```bash
railway login
railway init
```

#### 2. Deploy Producer

```bash
railway up --service producer
```

#### 3. Deploy Consumer

```bash
railway up --service consumer
```

#### 4. Configurar variáveis de ambiente

No Railway Dashboard:
- Selecione cada serviço (producer/consumer)
- Vá em "Variables"
- Adicione todas as variáveis do `.env`

#### 5. Verificar logs

```bash
railway logs --service producer
railway logs --service consumer
```

---

## 📁 Estrutura do Projeto

```
weather-data-pipeline/
│
├── producer/
│   ├── main.py              # Script principal do producer
│   ├── Dockerfile           # Container do producer
│   └── requirements.txt     # Dependências do producer
│
├── consumer/
│   ├── main.py              # Script principal do consumer
│   ├── Dockerfile           # Container do consumer
│   └── requirements.txt     # Dependências do consumer
│
├── common/
│   ├── __init__.py
│   ├── apiclient.py         # Client da OpenWeatherMap API
│   ├── kafkaclient.py       # Client do Kafka
│   └── supabaseclient.py    # Client do Supabase
│
├── config/
│   └── locations.json       # Lista de cidades para monitorar
│
├── .env.example             # Template de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Este arquivo
└── requirements.txt        # Dependências globais
```

---

## 📊 Dashboards

### Grafana - Como Conectar

1. **Adicionar Data Source**
   - Type: PostgreSQL
   - Host: `seu-projeto.supabase.co:5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: (sua senha do Supabase)
   - SSL Mode: `require`

2. **Importar Dashboards**

Crie painéis com estas queries:

#### Temperatura ao longo do tempo
```sql
SELECT 
  created_at as time,
  temperatura_celsius
FROM weather_metrics
WHERE city = '${Cidade}'
  AND $__timeFilter(created_at)
ORDER BY time
```

#### Média de temperatura
```sql
SELECT 
  AVG(temperatura_celsius) as "Temperatura Média"
FROM weather_metrics
WHERE city = '${Cidade}'
  AND $__timeFilter(created_at)
```

#### Mapa geográfico
```sql
SELECT DISTINCT ON (city)
  created_at as time,
  city,
  latitude,
  longitude,
  temperatura_celsius
FROM weather_metrics
WHERE $__timeFilter(created_at)
ORDER BY city, created_at DESC
```

### Variável Dropdown (Filtro de Cidade)

**Name:** `Cidade`
**Type:** Query
**Query:**
```sql
SELECT DISTINCT city FROM weather_metrics ORDER BY city
```

---

## 🐛 Troubleshooting

### Producer não envia mensagens

**Problema:** Erro de autenticação no Kafka

**Solução:**
```bash
# Verificar credenciais do Kafka
echo $KAFKA_SASL_USERNAME
echo $KAFKA_SASL_PASSWORD

# Testar conectividade
telnet seu-broker.confluent.cloud 9092
```

### Consumer não processa mensagens

**Problema:** Offset do consumer está no final

**Solução:**
```python
# Em kafkaclient.py, adicionar:
'auto_offset_reset': 'earliest'  # Ler desde o início
```

### Dados NULL no banco

**Problema:** Campo latitude/longitude NULL

**Solução:**
- Verificar se `locations.json` tem campos `lat` e `lon`
- Verificar logs do producer para confirmar coleta
- Verificar se tabela tem colunas `latitude` e `longitude`

### Gráfico serrilhado no Grafana

**Problema:** Muitos pontos de dados

**Solução:**
```sql
-- Usar time_bucket para agregar
SELECT 
  time_bucket('1 hour', created_at) AS time,
  AVG(temperatura_celsius) as temp
FROM weather_metrics
WHERE $__timeFilter(created_at)
GROUP BY time_bucket('1 hour', created_at)
ORDER BY time
```

### Logs de Debug

Adicionar ao código:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🗺️ Roadmap

### Versão 1.0 (Atual)
- [x] Producer para coleta de dados
- [x] Consumer para persistência
- [x] Dashboards básicos no Grafana
- [x] Deploy no Railway

### Versão 2.0 (Próxima)
- [ ] Adicionar mais campos (UV index, sensação térmica)
- [ ] Implementar alertas (temperatura > 35°C)
- [ ] API REST para consultar histórico
- [ ] Testes unitários e de integração

### Versão 3.0 (Futuro)
- [ ] Machine Learning para previsão
- [ ] Data Quality checks
- [ ] Migrar para Avro (em vez de JSON)
- [ ] Implementar CDC (Change Data Capture)
- [ ] Multiple consumers para diferentes processamentos

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes

- Siga PEP 8 para código Python
- Adicione docstrings em funções
- Mantenha commits pequenos e descritivos
- Teste localmente antes de criar PR

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@ElomMaio98](https://github.com/ElomMaio98)
- LinkedIn: [elom-maio](https://www.linkedin.com/in/elom-maio)
- Medium: [@seu-usuario](https://medium.com/@seu-usuario)

---

## 🙏 Agradecimentos

- [OpenWeatherMap](https://openweathermap.org/) - API de dados meteorológicos
- [Confluent](https://www.confluent.io/) - Kafka gerenciado
- [Supabase](https://supabase.com/) - PostgreSQL gerenciado
- [Grafana](https://grafana.com/) - Plataforma de visualização
- [Railway](https://railway.app/) - Deploy simplificado

---

## 📚 Recursos Adicionais

- [Documentação Kafka](https://kafka.apache.org/documentation/)
- [TimescaleDB Docs](https://docs.timescale.com/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Artigo no Medium](link-do-seu-artigo) - Explicação detalhada do projeto

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**