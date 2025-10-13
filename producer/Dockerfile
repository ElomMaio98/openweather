# 1. Start with the lightweight Python image.
FROM python:3.9-slim

# 2. Set the working directory.
WORKDIR /app

# 3. THIS IS THE FIX: Copy the producer's specific requirements file
#    and rename it to "requirements.txt" inside the container.
COPY requirements-producer.txt requirements.txt

# 4. Now, pip can install from the newly copied requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project code.
COPY . .

# 6. Set the start command.
CMD ["python", "producer/main.py"]
