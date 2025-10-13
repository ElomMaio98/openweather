# Usa uma imagem Python mais completa
FROM python:3.9-bullseye

# Instala as ferramentas de compilação
RUN apt-get update && apt-get install -y build-essential

# O resto do arquivo permanece o mesmo...
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando específico para cada serviço
# (CMD ["python", "consumer/main.py"] ou CMD ["python", "producer/main.py"])

# Comando que será executado quando o container iniciar
CMD ["python", "consumer/main.py"]
