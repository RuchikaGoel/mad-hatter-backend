# Use the official Python image
FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command to run the service
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
