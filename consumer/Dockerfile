FROM python:3.9-slim

WORKDIR /app

# Copia o requirements.txt da raiz do projeto
COPY ../requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta common (necessária!)
COPY ../common ./common

# Copia o código do consumer
COPY . .

# Comando para rodar
CMD ["python", "main.py"]