# 1. Start with the lightweight Python image.
FROM python:3.9-slim

# 2. Set the working directory.
WORKDIR /app

# 3. THIS IS THE FIX: Copy the consumer's specific requirements file.
COPY requirements-consumer.txt requirements.txt

# 4. Install the consumer's dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project code.
COPY . .

# 6. Set the start command.
CMD ["python", "consumer/main.py"]
