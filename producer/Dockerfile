# 1. Imagem Base: Comece com um ambiente Python 3.9 leve.
FROM python:3.9-slim

# 2. Diretório de Trabalho: Crie uma pasta /app e entre nela.
WORKDIR /app

# 3. Copie a lista de dependências primeiro para aproveitar o cache do Docker.
# O ponto final significa "copie para o diretório de trabalho atual (/app)".
COPY requirements.txt .

# 4. Instale as dependências listadas no requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie todo o resto do seu código (pastas common, config, etc.) para o /app.
COPY . .

# 6. Comando de Execução: Quando o container iniciar, rode este comando.
# Esta é a linha que diz ao Railway "Este é o serviço do PRODUTOR".
CMD ["python", "producer/main.py"]