# Usa uma imagem Python leve como base
FROM python:3.9-slim

# ----> ADIÇÃO IMPORTANTE AQUI <----
# Atualiza a lista de pacotes do sistema e instala as ferramentas de compilação.
# O '-y' responde 'sim' para todas as perguntas.
RUN apt-get update && apt-get install -y build-essential

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto
COPY . .

# Comando que será executado quando o container iniciar
CMD ["python", "consumer/main.py"]
