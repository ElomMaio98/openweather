# 1. Usamos a mesma imagem base leve.
FROM python:3.9-slim

# 2. Definimos o diretório de trabalho.
WORKDIR /app

# 3. Copiamos APENAS a lista de requisitos do consumer.
COPY requirements-consumer.txt requirements.txt

# 4. Instalamos as dependências do consumer. Sem compilação, sem Flink.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo o código do projeto.
COPY . .

# 6. Definimos o comando para iniciar o consumer.
CMD ["python", "consumer/main.py"]
