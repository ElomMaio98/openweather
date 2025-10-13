# 1. Imagem Base: Comece com um ambiente Python 3.9 leve.
FROM python:3.9-slim

# 2. Diretório de Trabalho: Crie uma pasta /app e entre nela.
WORKDIR /app

# 3. Copie e instale as dependências.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie todo o resto do seu código para o /app.
COPY . .

# 5. Comando de Execução: A diferença crucial está aqui.
# Esta linha diz ao Railway "Este é o serviço do CONSUMIDOR".
CMD ["python", "consumer/main.py"]