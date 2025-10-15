-- Remove a tabela se já existir (útil para testes)
DROP TABLE IF EXISTS weather_metrics;

-- Cria a tabela de métricas do clima
CREATE TABLE weather_metrics (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature_celsius FLOAT NOT NULL,
    humidity INTEGER NOT NULL,
    pressure INTEGER NOT NULL,
    wind_speed FLOAT NOT NULL,
    timestamp_unix BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria índices para otimizar queries
CREATE INDEX idx_city ON weather_metrics(city);
CREATE INDEX idx_timestamp ON weather_metrics(timestamp_unix);
CREATE INDEX idx_created_at ON weather_metrics(created_at);

-- Comentários nas colunas (documentação)
COMMENT ON TABLE weather_metrics IS 'Métricas meteorológicas das capitais brasileiras';
COMMENT ON COLUMN weather_metrics.city IS 'Nome da cidade';
COMMENT ON COLUMN weather_metrics.temperature_celsius IS 'Temperatura em graus Celsius';
COMMENT ON COLUMN weather_metrics.humidity IS 'Umidade relativa do ar (%)';
COMMENT ON COLUMN weather_metrics.pressure IS 'Pressão atmosférica (hPa)';
COMMENT ON COLUMN weather_metrics.wind_speed IS 'Velocidade do vento (m/s)';
COMMENT ON COLUMN weather_metrics.timestamp_unix IS 'Timestamp Unix da medição pela API';
COMMENT ON COLUMN weather_metrics.created_at IS 'Data/hora de inserção no banco de dados';