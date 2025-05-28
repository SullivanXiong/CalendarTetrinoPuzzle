# Use an official Python image as the base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (optional: needed for pip or grpc)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

ENV PYTHONPATH=/app

# Expose the gRPC server port (e.g., 50051)
EXPOSE 50051

# Define the default command to run your server
CMD ["python", "calendar_solver/server/grpc_server.py"]
