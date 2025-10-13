# 1. Imagem Base: Comece com a imagem oficial do Flink que já inclui Python.
FROM apache/flink:1.17-scala_2.12-java11

# O diretório de trabalho padrão do Flink já é /opt/flink, então não precisamos mudar.

# 2. Crie uma pasta dedicada para nossos scripts Python e JARs de dependência.
# Isso mantém nosso código organizado e separado dos binários do Flink.
WORKDIR /opt/flink/usrlib

# 3. Copie o arquivo de dependências Python.
COPY requirements.txt .

# 4. Instale as dependências Python no ambiente do container.
# O Flink precisa ter acesso a bibliotecas como 'psycopg2-binary'.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie as pastas com nosso código customizado para dentro do container.
COPY common/ ./common
COPY processor/ ./processor

# 6. Copie os JARs dos conectores para a pasta de bibliotecas principal do Flink.
# O Flink automaticamente carrega qualquer JAR que esteja nesta pasta.
COPY flink_jars/flink-sql-connector-kafka-3.0.1-1.17.jar /opt/flink/lib/
COPY flink_jars/postgresql-42.7.1.jar /opt/flink/lib/

# 7. Comando de Execução: A instrução final para o Railway.
# Este comando inicia o Flink em modo de aplicação, submetendo nosso job.
# As variáveis de ambiente (como o endereço do JobManager) serão passadas pelo Railway.
CMD ["flink", "run", "-py", "/opt/flink/usrlib/processor/flink_job.py"]