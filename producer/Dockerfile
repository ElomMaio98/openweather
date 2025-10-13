# 1. Começamos com a imagem Python mais leve e eficiente.
FROM python:3.9-slim

# 2. Definimos o diretório de trabalho.
WORKDIR /app

# 3. Copiamos APENAS a lista de requisitos do producer,
#    renomeando-a para 'requirements.txt' dentro do container.
COPY requirements-producer.txt requirements.txt

# 4. Instalamos somente as poucas dependências que o producer precisa.
#    Este passo será muito rápido agora.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo o código do projeto.
COPY . .

# 6. Definimos o comando para iniciar o producer.
CMD ["python", "producer/main.py"]
